# Top-20 проверок: бизнес-риски и уязвимости

Не полный регресс. Только то, что при провале = потеря денег, обход правил или ложные цифры для пользователей/админов.

Формат: **функция → риск → что сделать → pass**.

---

## 1. Unstake / Lock

**Риск:** вывод до конца лока / обход UI.  
**Проверка:** unstake до unlock через UI и через raw tx.  
**Pass:** оба пути reject; в ошибке — exact unlock date.

---

## 2. Чужие позиции (IDOR)

**Риск:** claim / compound / unstake с чужого PDA.  
**Проверка:** подменить position account в перехваченной tx, подписать своим ключом.  
**Pass:** on-chain reject; жертва без изменений.

---

## 3. Подмена destination

**Риск:** вывод на ATA атакующего.  
**Проверка:** в unstake/claim подставить чужой token account.  
**Pass:** reject; токены только на ATA владельца позиции.

---

## 4. Double-spend (race)

**Риск:** два unstake / claim+unstake = двойная выплата.  
**Проверка:** две tx на одну позицию почти одновременно.  
**Pass:** успех ровно один; второй fail; баланс сходится с формулой.

---

## 5. Claim в lock

**Риск:** claim ломает unlock/tier или «съедает» principal.  
**Проверка:** claim на locked-позиции.  
**Pass:** rewards ушли; principal на месте; unlock date и tier те же.

---

## 6. Auto-compound at unlock

**Риск:** двойной auto-compound или потеря rewards.  
**Проверка:** дождаться unlock без claim; через неделю снова посмотреть base.  
**Pass:** +unclaimed ровно один раз; второго add нет.

---

## 7. Manual compound в lock

**Риск:** UI запрещает, контракт пускает (обход).  
**Проверка:** raw compound на locked-позиции.  
**Pass:** on-chain reject (если по спеке нельзя). Если пускает — баг/уточнение у команды.

---

## 8. Пустой reward pool

**Риск:** потеря accrued или «вечный» долг без выхода.  
**Проверка:** обнулить vault → claim → unstake.  
**Pass:** claim rewards fail, accrued сохранён; unstake даёт выбор wait / principal-only с confirm обоих amounts.

---

## 9. Restrictions (principal / reward)

**Риск:** заблокированный кошелёк всё равно выводит.  
**Проверка:** principal-ban → unstake; reward-ban → unstake.  
**Pass:** principal-ban = unstake нельзя; reward-ban = только principal + явный confirm о безвозвратной потере rewards.

---

## 10. Pause не ловит средства

**Риск:** pause = rug для уже застейкавших.  
**Проверка:** pause → claim / unstake (после unlock) / compound.  
**Pass:** выводы работают; новые stake и check-in — нет; accrual стоит.

---

## 11. Daily check-in / UTC

**Риск:** два check-in в «один день» или пропуск границы → раздутый rate.  
**Проверка:** второй check-in в тот же UTC day; пара 23:50 + 00:10 UTC.  
**Pass:** same-day = reject; через полночь = 2 шага; Clock on-chain, не часы устройства.

---

## 12. Rate / streak после miss и unstake

**Риск:** miss не сбрасывает rate; или streak сбрасывается при restake → неверная экономика.  
**Проверка:** пропустить UTC day; unstake → сразу stake снова.  
**Pass:** miss → rate = tier min со следующего day, старые accrued целы; streak после restake сохранён, tier снова primary.

---

## 13. Stake: валидация amount

**Риск:** stake > balance / 0 / ниже min уходит в подпись и ломает учёт.  
**Проверка:** три кейса до signature + raw tx с 0.  
**Pass:** UI блок до sign; on-chain тоже reject на 0/ниже min.

---

## 14. Независимость позиций + иммутабельный unlock

**Риск:** merge позиций или сдвиг unlock после pause/смены конфига.  
**Проверка:** 3 stake; pause; поднять min lock; сравнить unlock.  
**Pass:** 3 отдельные позиции; unlock дат не двигаются.

---

## 15. Caps (после решения PO) / CFG-08

**Риск:** один кошелёк забирает пул; или cap считается от pool total.  
**Проверка:** stake сверх per-wallet 500k и сверх global 30M (когда enforced).  
**Pass:** on-chain reject; per-wallet смотрит **сумму кошелька**, не TVL пула.

---

## 16. Admin config: единицы измерения

**Риск:** админ вводит «6%» / «1500 MEX» → on-chain улетает неверный BPS/base units → чужие rates/caps.  
**Проверка:** задать 6.00%, 7 days, 1,500 MEX → decode payload / on-chain.  
**Pass:** 600 BPS; seconds = 7×86400; amount = 1500×10⁹; silent u64 wrap отсутствует.

---

## 17. Mainnet deploy order + upgrade authority

**Риск:** wrong program / потеря upgrade path / второй mint.  
**Проверка:** rehearsal на devnet: prep gates → steps 1–9; create pool **до** transfer authority; step 9 к non-signing vault PDA.  
**Pass:** каждый gate зелёный; hash match; authority on-chain = vault PDA; mint без freeze, без race второго токена.

---

## 18. Indexer = правда для UI

**Риск:** дашборд врёт → юзер принимает решения по фейковым rewards/TVL.  
**Проверка:** stake/claim/unstake → сравнить DB и Explorer ≤ 1 мин; restart индексера.  
**Pass:** цифры совпадают с on-chain; нет dup/loss после restart.

---

## 19. Утечка секретов / wrong network

**Риск:** слив Helius key; stake не в той сети.  
**Проверка:** DevTools — нет `api-key` в front RPC URL; connect на wrong cluster.  
**Pass:** RPC через backend/proxy; wrong network → warn + money-tx не собираются.

---

## 20. UI-суммы vs on-chain (доверие и ошибки оператора)

**Риск:** round-up в Total/confirm → расхождение с Explorer, ложные баги поддержки, скрытые ошибки админ-вводов.  
**Проверка:** stake 1500.1999 (или любой «хвост»); сверить confirm, Success, таблицу, Total, Explorer.  
**Pass:** везде truncate вниз; Total = сумма строк; Explorer = raw truth.

---

## Быстрый порядок (один прогон)

1. Wrong network + Helius key (#19)  
2. Stake valid + invalid amounts (#13, #14)  
3. Check-in UTC / miss / restake streak (#11, #12)  
4. Claim в lock (#5)  
5. Unlock → auto-compound once (#6)  
6. Manual compound lock bypass (#7)  
7. Unstake lock + IDOR + destination + race (#1–#4)  
8. Empty pool + restrictions + pause (#8–#10)  
9. Caps / admin units (#15, #16)  
10. Indexer sync (#18)  
11. UI rounding (#20)  
12. Deploy rehearsal (#17) — отдельно, до mainnet  

---

## Покрытие по функциям

| Функция | Чеки |
|---|---|
| Stake | #13, #14, #15 |
| Check-in / rate | #11, #12 |
| Claim | #2, #4, #5, #8, #9 |
| Compound | #6, #7 |
| Unstake | #1, #2, #3, #4, #8, #9, #10 |
| Pause / admin | #10, #16 |
| Deploy / secrets | #17, #19 |
| Indexer / UI truth | #18, #20 |
