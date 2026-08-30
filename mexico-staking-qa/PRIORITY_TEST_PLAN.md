# Mexico (MEX) — приоритетный план проверок

По тикетам. Два блока: **функционал** и **UI**. Внутри: **P0 → P1 → P2**.  
Правило: для money-операций проверять **и UI, и on-chain** (фронт — подсказка).

---

# A. Функциональные проверки

## A-P0. Деньги, lock, mainnet, данные

### 1. Claim / Compound / Unstake
| Проверить | Ожидание |
|---|---|
| Unstake до unlock | UI блокирует; raw tx отклоняется с exact unlock date |
| Claim в lock | Rewards на кошелёк; principal на месте; unlock/tier не меняются |
| Auto-compound at unlock | Ровно 1 раз: base = principal + unclaimed; дальше без повторного add |
| Manual compound | Только unlocked; base += accrued; accrued → 0; без нового lock |
| Full unstake | Principal + rewards одной tx; позиция закрыта; другие не тронуты |
| Pause | Claim/compound/unstake **работают**; stake/check-in/accrual — нет |
| Restrictions | Principal-ban → unstake нельзя; reward-ban → principal only + явный confirm о потере rewards |
| Пустой reward pool | Claim rewards fail, accrued сохраняется; unstake: wait **или** principal-only с confirm обоих amounts |
| Fail paths | Reject / failed tx → состояние без изменений |
| Security | Чужая позиция / подмена destination / double-unstake race → reject, без double payout |

### 2. Stake (Deposit)
| Проверить | Ожидание |
|---|---|
| Happy path | Списание = amount; 1 новая позиция; unlock = показанный в confirm |
| Независимость | 3 stake → 3 позиции, 3 разных unlock; без merge |
| Валидация до sign | > balance / < min / 0 / нет SOL на fee → блок, без signature |
| Иммутабельность unlock | Pause и смена min lock в конфиге **не** двигают старые unlock |
| Pause / pool | При pause stake нельзя; при пустом reward pool — можно |
| Restrictions | Principal-ban **не** мешает stake |
| Fail paths | Cancel / fail → баланс и позиции без изменений |

### 3. Daily Check-in & Rate
| Проверить | Ожидание |
|---|---|
| Scope | 1 check-in на кошелёк/день; поднимает rate **всех** active positions (в т.ч. 50 шт. = 1 tx) |
| UTC | Второй check-in в тот же UTC day — reject; 23:50 + 00:10 = 2 шага |
| Прогрессия | Без check-in = tier min (не 0); +1pp/день до max; дальше держится max |
| Miss | Пропущенный UTC day → reset к min со следующего; прошлые accrued не трогать |
| Tiers | После unlock → secondary (2.5–5%) без действия; locked+unlocked → разные rates при одном streak |
| Pause | Дни pause ≠ miss, rate не reset |
| Accrual | Растёт между reload; rate меняется только forward; display = estimate, exact на claim/compound/unstake |
| Access | Нет позиции / pause → check-in недоступен; device clock не влияет |

### 4. Mainnet deploy (runbook)
| Проверить | Ожидание |
|---|---|
| Prep | ≥3.32 SOL outright; mint без freeze; Squads + vault index 0; vault ATA mint уже есть |
| Tooling | Pool-create читает **config file**, не fixture; missing field → refuse |
| Order | Шаги 1→9 с gate на каждом; **create pool (7) до transfer upgrade authority (9)** |
| Rehearsal | Step 9 на **devnet** к non-signing vault PDA (нужный CLI flag) → on-chain OK **до** mainnet |
| Extra | Hash match step 4; mint-race (аудит HIGH); mainnet key ≠ leaked front Helius key |

### 5. Indexer
| Проверить | Ожидание |
|---|---|
| Events | stake, check-in, claim, compound (manual+auto), unstake, admin config, pause/resume |
| Latency | Confirm → DB ≤ 1 мин |
| Truth | Position / wallet rate&streak / TVL&reward pool = on-chain |
| Resilience | Restart → backfill без loss/dup; WS duplicates не плодят double history |

### 6. Tokenomics caps (сначала решение PO)
Без решения PO — кейсы **Blocked**, не Pass.

| Лимит | После «implement» | После «remove» |
|---|---|---|
| Global 30M | On-chain reject сверх капа; unstake frees room | Убрать из UI/доков |
| Per-wallet 500k | Сверка со **стейком кошелька**, не pool total (CFG-08) | То же |
| Occupancy | «Spots remaining» live | Не строить |

---

## A-P1. Ядро продукта

### 7. Landing + Web Frontend (логика)
- Connect: Phantom + ≥1 другой; wrong network → warn + нельзя stake; disconnect сразу прячет balances/positions/history.
- Публично: terms (rate/lock/check-in) из **live config**; TVL, holders, staked, activity — с бэка; Token Price — реальный фид или явный Pending (не фейк).
- Виджет: inactive до connect; клик → wallet prompt.
- E2E на devnet: stake → check-in → claim → compound → unstake.
- History: хронология, See TX → explorer, filter по типу, empty «No transactions found».
- Confirm/validation **до** signature.

### 8. Dashboard: My Positions + History
- Только с connected wallet; header = masked address + disconnect.
- 3 cards (Total Staked / Earned / APR) — live, без reload; APR из config (Figma 35% vs docs 10% → config wins, завести баг на макет).
- **Locked:** Reinvest + Claim; Unstake нет/disabled. **Unlocked:** Unstake + Reinvest + Claim.
- Lock Remains: countdown → auto `UNLOCKED` без reload.
- Rewards: `$0` без «+»; иначе зелёный `+$…`.
- History: `+` зелёный / `−` красный; USD нейтральный; filter; Max = полный MEX balance.
- Суммы MEX/USD = API, без drift округления; много строк — scroll/pagination (уточнить у команды).

### 9. Action Modals (логика)
- Триггер верный; сумма = input (Stake) или accrued (Claim/Reinvest).
- Текст lock = **7 days из config** (не 10 с Figma).
- Success только после on-chain confirm; Failure — единый copy.
- X / Continue / Return — без side effects; dashboard обновлён.
- Check-in modal **не** открывать при disconnected / без позиции (design bug на макете).
- Day 1–7 «100…700 MEX» на макете ≠ PRD rate logic — не хардкодить как бизнес-правило.

### 10. Modal load / Check-in cells / Unstake missing
- First open / slow net: **skeleton**, не куски контента; reopen (cache) — сразу полный.
- Check-in history: каждая day cell = defined state, never empty (race).
- Unstake: в ожидаемом state есть и работает (регрессия «пропал» закрыта).

### 11. Audio (правила)
- Звук stake/claim/compound/unstake — **только после confirm**; на submit/pending/page load — тишина.
- Mute persists reload/return; muted → тишина, visual success остаётся.
- Опционально Connect / Check-in / Reinvest — те же правила.

### 12. Admin Config refactor
- 4 cards: Primary / Secondary / Time&Limits / Platform&Safety.
- Input → payload: `%`→BPS (×100); time units→seconds; MEX→×10⁹; helpers показывают raw.
- Validation до propose; hard limits по unit.
- Перед mainnet: defaults = PRD, не devnet fixtures; caps disabled пока PO не решил.
- После execute: on-chain = intent; нет silent u64 wrap (аудит).

### 13. Empty state (wallet connected, 0 positions)
| Header | Positions | MEX balance | UI |
|---|---|---|---|
| Address видна | Пусто | 0 | «No positions yet» + виджет «No MEX…» + Buy DEX |
| Address видна | Пусто | > 0 | «No positions yet» + активный Stake |
| Connect Wallet | — | — | Отдельный disconnected copy — **не** этот экран |

### 14. Admin: Stakers table
- Все wallets с ≥1 position: address (mask), #positions, total **principal** (уточнить vs +accrued), Status Active/Restricted.
- Sort ASC/DESC; row → detail; status обновляется после restriction; pagination.
- Non-admin не меняет restrictions.

---

## A-P2. После ядра

- **Splash:** до конца шагов 1–4 клики/wallet не работают; после — fully interactive; при slow net не застревает forever.
- **Feed/stats:** новые events без full reload; после sync индексера нет вечных 0/placeholder.
- **Token Price / final assets / caps UI** — когда есть фид / дизайн / решение PO.

---

# B. UI проверки

## B-P0. Врёт о деньгах или ломает действие

| # | Что | Pass если |
|---|---|---|
| 1 | **Округление MEX** | Confirm / Success / таблица / Total Staked — truncate вниз, одна precision; Total = сумма строк; on-chain raw = правда; в amounts тикер **MEX** текстом |
| 2 | **Empty vs Connect** | Connected+0 pos ≠ copy «CONNECT WALLET…»; виджет 0 MEX ≠ has MEX |
| 3 | **Lock / Unstake UI** | Locked: Unstake нет/disabled + unlock date; Unlocked: Unstake видим; модалки пишут **7 days** |
| 4 | **Success timing** | Confetti/Success только после confirm; pending без Success flash |
| 5 | **Loading / cells** | Skeleton на slow first open; day cells без пустых/мигающих дыр |

## B-P1. Основной UX

### Landing
Header (logo / 4 ticket-nav→PDF / Connect золотой) · hero + CTA · coin ambient · inactive stake card · 5 stats · activity scroll · кактусы hover (desktop) · **mobile adaptive по Figma**.

### Splash (визуал + perf)
1) Сцена + 3 loop (орнамент CW, sun pulse, блик по монете) параллельно · 2) 3D logo · 3) Header · 4) Контент.  
Mobile: стабильный FPS, нет freeze; offscreen — желательно pause loops.

### Dashboard
Tabs My Positions / History · цвета rewards/history · countdown layout · 2 vs 3 action buttons без overflow на mobile · filter + empty · Max + валидации виджета.

### Modals
Check-in: Day1–7, current red, future dim · Stake/Reinvest/Claim/Success/Failure по макету · X везде · mobile · check-in не при disconnect.

### Audio / Admin UI
Mute control видимый и переживает reload · Config: 4 cards, separators, payload helpers · Stakers: mask+hover, sort icons, status colors, pagination; detail лучше route `/admin/wallets/<addr>`.

## B-P2. Polish
Тикер **MEX** в amounts / **MEXICO** в brand · empty-state copy разный (личный vs admin) · **Android MWA** («could not reach…») · hitbox: декор не перекрывает CTA · prefers-reduced-motion.

## B-P3. Ждёт внешнее
Final Mexican assets · FigJam pixel-pass · Token Price card после фида.

---

# Порядок прогона

1. **A-P0 money:** stake → check-in → claim → unlock → auto-compound → manual compound → unstake (+ pause, restrictions, empty pool, IDOR).  
2. **Indexer** на тех же tx.  
3. **Mainnet runbook rehearsal** на devnet (особ. step 9).  
4. **A-P1** dashboard / modals / empty / audio / admin payloads.  
5. **B-P0** rounding + empty-state + 7 days + skeletons.  
6. **B-P1** landing + splash + mobile.  
7. **PO caps** → enforcement + occupancy.  
8. **B-P2/P3** polish.

---

# Тикет → приоритет

| Тикет | Функционал | UI |
|---|---|---|
| Claim / Compound / Unstake | **P0** | P0 amounts/unlock |
| Stake (Deposit) | **P0** | P0/P1 confirm |
| Daily Check-in & Rate | **P0** | P0 cells, P1 modal |
| Mainnet deploy | **P0** | — |
| Indexer | **P0** | данные UI |
| Tokenomics caps | **P0 decision** | occupancy после PO |
| Landing + Web Frontend | **P1** | **P1** |
| My Positions + History | **P1** | **P1** |
| Action Modals | **P1** | **P1** |
| Modal load / cells / Unstake missing | **P1** | **P0** |
| Audio | **P1** | **P1** |
| Admin Config | **P1** | **P1** |
| Empty state connected | **P1** | **P0** |
| Admin Stakers table | **P1** | **P1** |
| Splash intro | **P2** | **P1** |
| Android MWA / ticker polish | — | **P2** |

---

# Уже известные баги — куда бить

| Баг | Слот |
|---|---|
| Helius API key на фронте | A-P0 mainnet prep |
| UI rounding 1500.1999 → 1,500.20 vs 1,500.19 | **B-P0 #1** |
| Per-wallet cap vs pool total (CFG-08) | A-P0 caps + Admin Config |
| Reward Vault withdraw → multisig ATA, не личный wallet | Admin/Squads |
| Compound в lock: спека явна для unstake, не для compound | A-P0 — уточнить у команды |
| Empty-state copy / 10→7 days / check-in while disconnected | B-P0 / B-P1 |
| Android MWA | B-P2 |
