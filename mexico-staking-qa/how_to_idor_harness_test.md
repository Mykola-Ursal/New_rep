# Как проверить IDOR: claim / compound / unstake чужой позиции (Rust-харнес)

Цель теста: **программа отклоняет** ix, если `signer ≠ owner` позиции.  
Это defensive regression, не сценарий «как украсть».

Ниже — шаблон под типичный Anchor + `solana-program-test` / `anchor test`.  
Имена аккаунтов/ошибок подставьте из вашего `lib.rs` (у вас в саммари уже фигурирует путь к контракту).

---

## 0. Что открыть в коде до теста (5 минут)

В `accounts` структурах `Claim` / `Compound` / `Unstake` найдите, как задан владелец:

```rust
// типичные варианты — у вас будет один из них
#[account(mut, has_one = owner)]
pub position: Account<'info, Position>,

// или
#[account(
  mut,
  constraint = position.owner == owner.key() @ StakingError::InvalidAuthority
)]
pub position: Account<'info, Position>,

pub owner: Signer<'info>,
```

Запишите:

| Что | Значение у вас |
|---|---|
| Имя поля владельца на position | например `owner` / `authority` |
| Код ошибки | `ConstraintHasOne` (2001) **или** ваш `StakingError::…` |
| Как в тестах зовут хелпер stake | например `stake(&mut ctx, &owner, amount)` |

Дальше в шаблоне: `owner` = A, `attacker` = B.

---

## 1. Каркас теста

Положите рядом с остальными integration-тестами программы, например:

`programs/staking/tests/idor_wrong_signer.rs`  
или в уже существующий `tests/*.rs` / `#[tokio::test]` модуль харнеса.

Псевдоструктура (адаптируйте под ваш setup: `ProgramTest`, LiteSVM, `TestContext`):

```rust
use anchor_lang::prelude::*;
// ваши: TestContext, stake helper, claim/compound/unstake builders, error codes

#[tokio::test]
async fn reject_claim_compound_unstake_when_signer_is_not_position_owner() {
    // --- arrange ---
    let mut ctx = TestContext::new().await; // ваш bootstrap: program, mint, pool, clock

    let owner = Keypair::new();    // A — настоящий владелец позиции
    let attacker = Keypair::new(); // B — чужой signer

    // airdrop SOL + mint MEX обоим (как в ваших happy-path тестах)
    ctx.fund_wallet(&owner).await;
    ctx.fund_wallet(&attacker).await;

    // A создаёт позицию
    let position = ctx
        .stake(&owner, /* amount */ 1_000 * ONE_MEX, /* lock ok */)
        .await
        .expect("owner stake must succeed");

    // baseline до атаки
    let pos_before = ctx.fetch_position(&position).await;
    let owner_mex_before = ctx.token_balance(&owner).await;
    let attacker_mex_before = ctx.token_balance(&attacker).await;
    let vault_before = ctx.reward_vault_balance().await;

    // --- act + assert: каждая ix от B должна упасть ---
    for label in ["claim", "compound", "unstake"] {
        let result = match label {
            "claim" => ctx.claim_as(&attacker, &position).await,
            "compound" => ctx.compound_as(&attacker, &position).await,
            // для unstake: либо дождаться unlock в харнесе (warp clock),
            // либо ожидать СНАЧАЛА authority-ошибку (лучше), а не lock-ошибку
            "unstake" => ctx.unstake_as(&attacker, &position).await,
            _ => unreachable!(),
        };

        assert!(
            result.is_err(),
            "{label}: expected reject when signer != position.owner, got Ok"
        );
        assert_authority_error(&result, label);
    }

    // --- state unchanged ---
    let pos_after = ctx.fetch_position(&position).await;
    assert_eq!(pos_after, pos_before, "position account must be unchanged");
    assert_eq!(ctx.token_balance(&owner).await, owner_mex_before);
    assert_eq!(ctx.token_balance(&attacker).await, attacker_mex_before);
    assert_eq!(ctx.reward_vault_balance().await, vault_before);
}
```

---

## 2. Как собрать ix «от чужого signer»

Суть одна: **те же accounts, что у happy-path**, но:

- в метаданных `owner` / `authority` = pubkey **B**;
- в `signers` транзакции = **B** (и fee payer B);
- `position` = PDA/аккаунт позиции, созданной **A**.

Пример билдера (имена методов — как у вас в клиенте/CPI-хелпере):

```rust
impl TestContext {
    /// Claim от имени `signer`, по позиции `position` (может быть чужой).
    async fn claim_as(
        &mut self,
        signer: &Keypair,
        position: &Pubkey,
    ) -> Result<(), BanksClientError> {
        let accounts = Claim {
            owner: signer.pubkey(),          // <-- B
            position: *position,             // <-- позиция A
            // … pool, reward_vault, owner_ata, token_program, …
            // owner_ata: для B — его ATA (или даже ATA A — оба варианта должны fail
            // на authority; важнее не получить Success)
        };

        let ix = Instruction {
            program_id: self.program_id,
            accounts: accounts.to_account_metas(None),
            data: staking::instruction::Claim {}.data(),
        };

        let bh = self.banks.get_latest_blockhash().await.unwrap();
        let tx = Transaction::new_signed_with_payer(
            &[ix],
            Some(&signer.pubkey()),
            &[signer],
            bh,
        );

        self.banks.process_transaction(tx).await
    }

    // compound_as / unstake_as — тот же паттерн, другой instruction data + accounts
}
```

Если у вас уже есть `ctx.claim(&owner, &position)`, сделайте тонкую обёртку:

```rust
async fn claim_as(&mut self, signer: &Keypair, position: &Pubkey) -> Result<(), BanksClientError> {
    self.claim_with_authority(signer, position).await
}
```

и в production-пути тестов по-прежнему вызывайте `claim(&owner, …)`.

---

## 3. Как ассертить именно authority-ошибку

Недостаточно `is_err()`: на unstake до unlock err может быть про **lock**, и тест «зелёный», а IDOR не проверен.

```rust
fn assert_authority_error(result: &Result<(), BanksClientError>, label: &str) {
    let err = result.as_ref().err().expect("must be Err");
    let text = format!("{err:?}");

    // подставьте СВОЙ код из lib.rs / Anchor logs
    let ok = text.contains("ConstraintHasOne")
        || text.contains("InvalidAuthority")
        || text.contains("Unauthorized")
        || text.contains("ConstraintOwner")
        // || text.contains("Error Number: 6xxx")  // ваш кастомный код
        ;

    assert!(
        ok,
        "{label}: expected authority/owner error, got: {text}"
    );

    // явно НЕ принимаем как Pass для IDOR:
    assert!(
        !text.contains("LockNotExpired") && !text.contains("StillLocked"),
        "{label}: got lock error — warp clock first, иначе IDOR не проверен"
    );
}
```

**Для unstake:** перед вызовом от B либо:

1. `ctx.warp_to_unix_timestamp(pos_before.unlock_ts)` (или ваш helper), **потом** `unstake_as(attacker)`,  
   чтобы единственной причиной fail был wrong signer; **или**
2. оставить lock и отдельно завести кейс «wrong signer + still locked» только если в логах всё равно authority идёт **раньше** lock (зависит от порядка checks в программе — лучше warp).

---

## 4. Snapshot: что сравнить «до/после»

Минимум:

| Объект | Поля |
|---|---|
| Position account | `owner`, `amount` / principal, `unlock_ts`, `accrual_base`, `accrued` (как у вас названо) |
| ATA owner A | raw amount |
| ATA attacker B | raw amount |
| Reward vault ATA | raw amount |

Если позиция — PDA с закрытием на unstake: после failed unstake аккаунт **всё ещё существует** с теми же lamports/data.

---

## 5. Три отдельных теста (удобнее в CI)

Один комбинированный ок, но для читаемых падений лучше:

```text
idor_claim_rejects_wrong_signer
idor_compound_rejects_wrong_signer
idor_unstake_rejects_wrong_signer   // с warp past unlock
```

Плюс контрольный happy-path рядом (не в том же тесте):

```text
owner_can_claim_own_position   // sanity: A → claim → Ok
```

Иначе можно словить ложный Pass, если claim у всех сломан.

---

## 6. Команды запуска

Из корня Anchor-воркспейса программы (путь у команды):

```bash
# весь suite
anchor test

# только файл/фильтр по имени (зависит от runner)
cargo test -p staking --test idor_wrong_signer -- --nocapture
# или
anchor test -- --nocapture idor_
```

В логе при ожидаемом fail должны мелькать строки вроде:

```text
AnchorError … Error Code: ConstraintHasOne
# или
Program log: Error: InvalidAuthority
```

и **не** должно быть `TokenProgram: Transfer` success на ATA B.

---

## 7. Чеклист Pass / Fail

**Pass**

- [ ] claim от B → Err (authority)  
- [ ] compound от B → Err (authority)  
- [ ] unstake от B (после unlock) → Err (authority)  
- [ ] position A byte-for-byte / поля равны baseline  
- [ ] MEX A, MEX B, vault без изменений  
- [ ] claim от A (sanity) → Ok  

**Fail (баг)**

- любая ix от B вернула `Ok`  
- у B вырос MEX  
- позиция A изменилась / закрылась  
- err только про lock, а authority не проверялся  

---

## 8. Куда вписать в ваш процесс

| Слой | Роль |
|---|---|
| Этот харнес | закрывает on-chain IDOR (топ-20 #2) |
| UI: два Phantom | закрывает «не показать чужое» |
| Оба зелёные | можно ставить Pass в `TOP20_RISK_CHECKS` #2 |

Имена хелперов (`TestContext::stake`, `claim_as`) замените 1:1 на те, что уже есть в 579-кейсовом Rust-плане — логика теста не меняется: **тот же position, другой Signer**.
