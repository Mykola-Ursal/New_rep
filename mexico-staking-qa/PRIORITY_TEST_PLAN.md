# Mexico (MEX) — приоритетный план проверок по тикетам

Дата: 30 августа 2026.  
Источники: тикеты ниже + `CONTEXT.md` (аудит, UI-rounding, Reward Vault, 579-кейсовый план).

Два блока: **функциональные** и **UI**. Внутри каждого — приоритеты  
`P0` (блокер / деньги / mainnet) → `P1` (ядро продукта) → `P2` (важно, но не блокирует релиз-кандидат) → `P3` (polish / зависит от PO).

Принцип проверки контракта (сквозной): **фронт — подсказка; программа — источник правды**. Для money-операций дублировать проверку через UI и через raw instruction / Network tab.

---

## Блок A. Функциональные проверки

### A-P0 — деньги, lock, mainnet, индексер (делать первым)

#### 1. Claim / Compound / Unstake
**Тикет:** Claim / Compound / Unstake  
**Почему P0:** точка вывода средств; пересечение lock, автокомпаунда, restrictions, пустого reward pool.

**Acceptance criteria (из тикета + критичные дополнения):**
- [ ] Unstake до unlock заблокирован в UI **и** отклонён on-chain с указанием exact unlock date.
- [ ] Claim на locked-позиции работает; principal остаётся; accrued → 0; unlock date / tier не меняются.
- [ ] Auto-compound at unlock ровно **один раз**; позиция неделю после unlock без второго auto-add.
- [ ] Manual compound только на unlocked; base += accrued; accrued → 0; lock/tier не меняются.
- [ ] Unstake возвращает principal + rewards одной tx и закрывает только эту позицию.
- [ ] Pause **не** блокирует claim/compound/unstake (только stake/check-in/accrual).
- [ ] Principal restriction → unstake запрещён; reward restriction → unstake principal only после явного confirm о потере rewards.
- [ ] Пустой reward pool: claim rewards отклонён, accrued не теряется; на unstake — выбор wait / principal-only с confirm обоих amounts.
- [ ] Rejected signature / failed tx → позиция и баланс без изменений.
- [ ] IDOR: claim/compound/unstake чужой позиции отклонены on-chain.
- [ ] Race: двойной unstake / unstake+claim — без double payout.

**Что ещё важно проверить (вне AC тикета):**
- Destination ATA только владельца позиции (подмена destination).
- Rent refund при close position; соседние позиции не затронуты.
- Округление: on-chain amount = точное raw; UI truncate вниз (связь с UI-блоком).
- После unstake+restake streak сохраняется, tier снова primary.

---

#### 2. Staking (Deposit)
**Тикет:** Staking (Deposit)  
**Почему P0:** создание позиции — источник всех последующих money-flow.

**Acceptance criteria:**
- [ ] Валидный stake: списание ровно amount, одна новая позиция, корректный unlock date.
- [ ] 3 stake → 3 независимые позиции с независимыми unlock.
- [ ] Above balance / below min / zero — блок **до** signature.
- [ ] Unlock date в confirm = unlock date в позиции после confirm.
- [ ] Повышение min lock в конфиге **не** меняет unlock уже созданных позиций.
- [ ] Pause period **не** сдвигает unlock date.
- [ ] Stake успешен при пустом reward pool.
- [ ] Cancel signature / failed tx → баланс и позиции без изменений.
- [ ] Stake недоступен при pause; principal restriction **не** блокирует stake.
- [ ] Mainnet-only (или корректный network guard на фронте + on-chain env).

**Что ещё важно:**
- Недостаточно SOL на fee — понятная ошибка, позиция не создаётся.
- Нет merge позиций; нет скрытого per-position max (пока caps не приняты PO — см. §5).
- Concurrent stakes с одного кошелька — обе проходят или одна честно fails без corruption.

---

#### 3. Daily Check-in & Reward Rate
**Тикет:** Daily Check-in & Reward Rate (дубль в списке — один тикет)  
**Почему P0:** определяет payout; UTC boundary и tiers легко сломать.

**Acceptance criteria:**
- [ ] Один check-in поднимает rate **всех** active positions кошелька.
- [ ] 50 позиций = одна tx check-in.
- [ ] Второй check-in в тот же UTC day заблокирован (UI + on-chain).
- [ ] Без check-in accrual = tier minimum, не 0.
- [ ] 5 consecutive days: min→max по 1pp; дальше держится max.
- [ ] 23:50 UTC + 00:10 UTC = два шага.
- [ ] Rate с 09:00 действует до конца того же UTC day.
- [ ] Пропущенный UTC day → reset к min со следующего day; прошлые accrued не трогаются.
- [ ] Accrued растёт между reload без check-in.
- [ ] После unlock позиция сама переходит на secondary bounds.
- [ ] Locked + unlocked одновременно → разные rates при одном step streak.
- [ ] Pause days не считаются miss и не reset.
- [ ] Смена max rate в конфиге влияет только forward.

**Что ещё важно:**
- Check-in без active position — действие отсутствует.
- Device clock skew не влияет (on-chain Clock).
- Streak не сбрасывается unstake+restake.
- Displayed accrued = estimate; exact только на claim/compound/unstake.

---

#### 4. Investigate & Deploy → Mainnet
**Тикет:** Investigate & Deploy Staking Program and Token to Mainnet  
**Почему P0:** без зелёного runbook mainnet = деньги на неправильном контракте.

**Acceptance criteria:**
- [ ] Pool-creation tool читает **все** поля из config file; отказывается стартовать при missing field (не fixture).
- [ ] Upgrade-authority transfer rehearsed на **devnet** к non-signing vault PDA с нужным CLI flag; подтверждено on-chain **до** mainnet schedule.
- [ ] Каждый из 9 шагов проходит свой verification gate до следующего.
- [ ] Step 7 (create pool) verified **до** step 9 (upgrade authority transfer).
- [ ] Before step 1: ≥3.32 SOL outright; mint без freeze authority; Squads multisig + vault index 0; vault token account для mint существует.

**Что ещё важно (из аудита / CONTEXT):**
- Hash match step 4 — stop if mismatch.
- Mint race (HIGH аудита): нет окна для второго токена.
- Unused `@anchor-lang/core` / mint key hygiene на deploy-машине.
- После create pool: printed authority/mint/initial_funding vs intent.
- Step 8: multisig threshold reached before execute.
- Не смешивать mainnet Helius key с leaked front-end key (BUG-001).

---

#### 5. Self-Hosted Indexer
**Тикет:** Self-Hosted Indexer  
**Почему P0 для UI/API правды:** дашборд и history живут от индексера; рассинхрон = фейковые балансы.

**Acceptance criteria:**
- [ ] Connect RPC/WS, ловит events: stake, check-in, claim, compound (manual+auto), unstake, admin config, pause/resume.
- [ ] Каждая test-операция в DB ≤ 1 минуты после confirm.
- [ ] Per-position / per-wallet / global pool stats = on-chain.
- [ ] Restart → backfill без loss/duplication.

**Что ещё важно:**
- Reorg / duplicate WS events не плодят double history rows.
- Pause/resume корректно отражаются в rate/accrual views.
- После admin config change индексер не отдаёт stale caps/rates бесконечно.

---

#### 6. Missing Tokenomics limits (PO decision gate)
**Тикет:** Missing Tokenomics limits not covered in PRD  
**Почему P0 как decision, не как тест:** без решения нельзя честно тестировать caps.

**Acceptance criteria (после решения PO):**
- [ ] Global cap 30M: enforce on-chain; new stake блокируется при заполнении; unstake frees room.
- [ ] Per-wallet 500k: enforce по **wallet stake**, не pool-wide total (CFG-08 / аудит MEDIUM).
- [ ] Occupancy indicator появляется только если global cap принят; live %/spots remaining.
- [ ] Если PO снимает лимиты из Tokenomics — убрать из UI/доков, не оставлять «мёртвые» поля.

**До решения PO:** помечать связанные кейсы Blocked; не принимать «нет cap» как Pass.

---

### A-P1 — ядро продукта (сразу после P0)

#### 7. Web Frontend (E2E umbrella) + Landing page (функциональная часть)
**Тикеты:** Web Frontend; Landing page  

**Acceptance criteria (функционал):**
- [ ] Phantom + ≥1 другой wallet adapter connect/disconnect.
- [ ] Wrong network → warn; stake недоступен до переключения.
- [ ] Disconnect сразу прячет balances / positions / history.
- [ ] Landing без кошелька: live terms (rate, lock, check-in) из **live config**, не hardcode.
- [ ] TVL / activity feed / stats cards с бэкенда (не stub), кроме Token Price (3rd party TBD — зафиксировать источник или «Pending»).
- [ ] Stake widget inactive до connect; клик → wallet prompt.
- [ ] Stake / check-in / claim / compound / unstake E2E на **devnet**.
- [ ] Validation + confirm **до** signature request.
- [ ] History + explorer links; filter by type; empty → «No transactions found».

**Что ещё важно:**
- BTC ticker / Token Price: graceful degrade если API down (не ломает весь лендинг).
- Network guard не только toast — инструкция stake не должна собираться на wrong cluster.

---

#### 8. Staking Dashboard — My Positions + Staking History (логика)
**Тикет:** Staking ("My Positions"+"Staking History")

**Acceptance criteria (функционал):**
- [ ] Dashboard только с connected wallet; header = masked address + disconnect.
- [ ] 3 stat cards = реальные user data, live update без reload.
- [ ] Tabs My Positions / History переключают данные; active tab выделен.
- [ ] Locked row: только Reinvest + Claim; Unstake отсутствует/disabled.
- [ ] Unlocked row: Unstake + Reinvest + Claim.
- [ ] Lock Remains countdown → auto UNLOCKED без reload.
- [ ] Rewards USD: `$0` без «+» когда 0; зелёный `+$…` когда есть.
- [ ] History: знак/цвет направления; See TX → explorer; filter работает; empty state.
- [ ] Max в виджете = полный доступный MEX balance.
- [ ] Суммы MEX/USD синхронны с API **без расхождений округления**.

**Что ещё важно:**
- APR card: на Figma 35%, в docs 10% — брать **live config**, завести баг на рассинхрон макета.
- Много позиций: scroll/pagination — уточнить у команды и зафиксировать ожидаемое.
- Empty state при connected + 0 positions — см. отдельный тикет (§13), не путать с disconnected.

---

#### 9. Staking Action Modals (логика триггеров / сумм / on-chain timing)
**Тикет:** Staking Action Modals

**Acceptance criteria (функционал):**
- [ ] Каждая модалка только от корректного триггера.
- [ ] Сумма = user input (Stake) или system accrued (Reinvest/Claim).
- [ ] Lock text = **7 days** из live config (не 10 с Figma).
- [ ] Success **только после** on-chain confirmation.
- [ ] Failure унифицированный, без утечки внутренних деталей.
- [ ] X / Continue / Return — без side effects; dashboard с **обновлёнными** данными.
- [ ] Daily Check-in модалка **не** открывается при disconnected / без active position (design bug на макете).

**Что ещё важно:**
- Day 1–7 fixed amounts (100…700) на макете не в PRD — не хардкодить как бизнес-логику; сверить с rate progression.
- Reinvest = compound по PRD naming; проверить, что UI label не путает с отдельным продуктом.

---

#### 10. Modal progressive load / Check-in highlight / Unstake missing
**Тикет:** Modal Content Loads Progressively…  

**Acceptance criteria (функционал/reliability):**
- [ ] First open Stake/Reinvest: skeleton/loading, **не** fragmented content.
- [ ] Reopen (cached): сразу полный контент.
- [ ] Slow network: loading state на всём окне load.
- [ ] Check-in history: каждая day cell = defined state, never empty (race).
- [ ] Unstake control: либо присутствует и работает в ожидаемом state, либо absence подтверждена PRD (тикет: «Анстейк вже є» — регрессия: не пропал снова).

**Что ещё важно:**
- Воспроизводить на throttled 3G в DevTools + cold cache.
- Логировать environment, где «stable» vs «degraded» (сеть/RPC).

---

#### 11. Audio Feedback (функциональные правила, не звук как дизайн)
**Тикет:** Implement Audio Feedback

**Acceptance criteria:**
- [ ] Stake / Claim / Compound / Unstake → sound **только после** on-chain confirmation.
- [ ] На submit / pending — тишина.
- [ ] Page load — никогда autoplay.
- [ ] Mute persists across reload / later visit (same device).
- [ ] Muted: sound off, visual success notification остаётся.
- [ ] Опционально (если в scope): Connect wallet, Daily check-in, Reinvest — те же правила timing/mute.

**Что ещё важно:**
- Двойной confirm (два tx) ≠ два звука на один user action без причины.
- Browser autoplay policies: muted-by-default до первого user gesture — не ломать mute preference.

---

#### 12. Admin: Configuration Management refactor (payload correctness)
**Тикет:** Refactor Admin Configuration Management  
**Почему P1 функционал:** ошибка units = неверные rates/caps on-chain.

**Acceptance criteria:**
- [ ] 4 cards: Primary Tier / Secondary Tier / Time & Limits / Platform & Safety.
- [ ] % → BPS (×100) корректно в payload; helper показывает BPS.
- [ ] Lock duration + TVL interval: unit dropdown → raw seconds.
- [ ] Token amounts: human input + separators → ×10⁹ base units; helper payload.
- [ ] Pre-submit validation: missing/out-of-hard-limit блокирует propose.
- [ ] Перед mainnet: defaults/hard limits = final PRD, не devnet fixtures.

**Что ещё важно:**
- Per-wallet / global cap fields: не отправлять пока PO не принял (§6), или disabled + tooltip.
- Squads propose: payload decode на review совпадает с тем, что ввёл админ (не «тихий» wrap u64 — аудит MEDIUM).
- После execute: on-chain config = UI intent; индексер подхватывает.

---

#### 13. Stake Dashboard Empty State (логика привязки к header)
**Тикет:** Stake Dashboard: Empty State (Wallet Connected, No Positions)

**Acceptance criteria:**
- [ ] Header с address + My Positions empty → **"No positions yet"** (не copy «Connect Wallet…»).
- [ ] Виджет справа: MEX balance = 0 → **"No MEX found…"** + Buy MEX on DEX.
- [ ] Balance > 0, positions = 0 → активный input + Stake.
- [ ] Disconnected vs connected empty — **разные** экраны; не смешивать (design bug на Figma).

---

#### 14. Admin: Stakers Table in Wallet Lookup
**Тикет:** Admin Panel — Add Stakers Table…

**Acceptance criteria:**
- [ ] Таблица всех wallets с ≥1 position.
- [ ] Columns: masked address, #positions, total principal, Status Active/Restricted.
- [ ] Status обновляется после apply/remove restriction.
- [ ] Row click → full wallet detail.
- [ ] Sort ASC/DESC по sortable columns.
- [ ] Pagination / usable at scale.

**Что ещё важно:**
- Уточнить «Total position amount» = principal only vs principal+accrued — зафиксировать в AC до теста.
- Detail: block principal/reward withdrawal работает и отражается в Status.
- Нет IDOR: non-admin не читает/не меняет restrictions.

---

### A-P2 — важно, но после ядра

#### 15. Intro splash animation — функциональные гейты
**Тикет:** Вступний анімаційний блок  

**Acceptance criteria (не визуал, а поведение):**
- [ ] До конца splash страница **не** интерактивна (клики/wallet не проходят).
- [ ] После шага 4 (контент под хедером) — fully interactive; splash не блокирует повторно.
- [ ] Skip/interrupt (медленная сеть, background tab): не застревает в non-interactive forever.
- [ ] Ambient loops не блокируют main thread до «мертвого» UI (бюджет FPS — см. UI).

---

#### 16. Landing / Web Frontend — activity feed & stats freshness
- [ ] Live Staking Activity непрерывный scroll; новые events появляются без full reload.
- [ ] Stats cards не показывают 0/placeholder после успешного sync индексера.
- [ ] Token Price: пока источника нет — явный empty/pending, не фейковый `$0.00012`.

---

### A-P3 — зависит от PO / внешние зависимости

- [ ] Tokenomics caps / occupancy — только после PO (§6).
- [ ] Final Mexican visual assets — блокер дизайна, не логики (заметка в Web Frontend).
- [ ] Token Price 3rd-party source TBD.
- [ ] APR 35% Figma vs 10% docs — product confirmation → live config wins.

---

## Блок B. UI / UX проверки

### B-P0 — то, что врёт о деньгах или ломает действие

#### 1. Округление и подписи сумм MEX (сквозное)
**Контекст:** CONTEXT UI-rounding + AC «без розбіжностей округлення».

**Acceptance / checks:**
- [ ] Модалка confirm, Success, таблица позиций, Total Staked, History — **одинаковое** отображение: truncate вниз к выбранной precision.
- [ ] On-chain raw (Explorer) = источник правды; UI никогда не round-up.
- [ ] Total Staked = сумма строк таблицы (не «3,000.26 vs 3,000.25»).
- [ ] Поле ввода: тикер **MEX** видим текстом (не только иконка); везде тикер, не «MEXICO» в amount contexts.
- [ ] Leading zeros / paste bypass validation — отклоняются.

#### 2. Empty state vs Connect state (design bug)
- [ ] Connected + 0 positions → «No positions yet», **не** «CONNECT WALLET TO SEE POSITIONS».
- [ ] Disconnected → отдельный copy + Connect CTA.
- [ ] Виджет: 0 MEX vs has MEX — разные UI (Buy vs Stake).

#### 3. Lock / Unstake affordances
- [ ] Locked: Unstake отсутствует или disabled + показан unlock date.
- [ ] Unlocked: Unstake видим и кликабелен.
- [ ] Регрессия «Unstake missing» не возвращается.
- [ ] Модалки Stake/Reinvest: **7 days** из config, не 10 с Figma.

#### 4. Success / Failure timing UI
- [ ] Success + confetti **только** после confirm (синхронно с audio rules).
- [ ] Pending state между submit и confirm — без Success flash.
- [ ] Failure единый copy; Return/Continue обновляют данные.

#### 5. Modal loading UX
- [ ] Skeleton на first load / slow network; нет «прыгающих» фрагментов.
- [ ] Check-in day cells: нет пустых/мигающих undefined states.

---

### B-P1 — основной UX лендинга, дашборда, модалок, админки

#### 6. Landing page layout & navigation
- [ ] Все блоки рендерятся без wallet: header, hero, coin, inactive stake card, 5 stats, activity.
- [ ] Nav tickets (Home / Tokenomics / Whitepaper / Roadmap) → корректные PDF/targets.
- [ ] Connect Wallet справа, золотой стиль, визуально отделён.
- [ ] Кактусы по краям: hover desktop; на mobile — graceful (нет hover → не ломают layout).
- [ ] CTA: Buy on DEX / Read Whitepaper работают.
- [ ] Stake card inactive + prompt на клик.
- [ ] Tariff strip (7 Days / 35% Monthly) из live config.
- [ ] Activity continuous scroll + mobile OK.
- [ ] Ambient coin inherited from splash task.
- [ ] **Mobile adaptive** по основной Figma — отдельный проход viewport.

#### 7. Intro animation (визуал / perf)
- [ ] Step 1: desert scene + 3 parallel loops (ornament CW, sun pulse, coin sheen path) без конфликта кадров.
- [ ] Step 2: 3D MEXICO logo overlay, ещё non-interactive.
- [ ] Step 3: header appears (logo left, nav center, Connect right).
- [ ] Step 4: rest of landing; interactive.
- [ ] Mobile perf: стабильный FPS, нет thermal thrash / tab freeze; loops можно paused when offscreen (желательно).

#### 8. Dashboard UI
- [ ] Header: masked address + disconnect «x».
- [ ] «STAKE MEXICO» title styling consistent с лендингом.
- [ ] Tabs full-width, active state явный.
- [ ] Таблицы: колонки, цвета rewards/history, Lock Remains layout (countdown + LOCKED / UNLOCKED).
- [ ] Actions: 2 vs 3 кнопки по state без overflow/overlap на mobile.
- [ ] Filter UI в History понятный; empty «No transactions found».
- [ ] Right stake widget: Max, MEX label, validation messages.

#### 9. Modals UI
- [ ] Daily Check-in: garland, Day 1–7 cards, current day red, future dimmed; кнопка claim.
- [ ] Accessibility: не показывать check-in UI при disconnected (design bug).
- [ ] Confetti только на Success; не на Failure.
- [ ] Close «X» на всех; focus trap / ESC (желательно).
- [ ] Mobile adaptive всех модалок.

#### 10. Audio UX
- [ ] Mute control discoverable; state reflected visually.
- [ ] Mute survives reload (DoD).
- [ ] Звуки: Claim ≈4–5s coins; Stake/Unstake clink assets из тикета; громкость не клиппит.

#### 11. Admin Configuration UI
- [ ] 4 visual cards, readable hierarchy.
- [ ] Helpers: «On-chain payload: N BPS / base units».
- [ ] Unit dropdowns обновляют hard-limit hints.
- [ ] Thousand separators; нет «сырого» 1500000000000 как единственного UX.
- [ ] Warning: defaults = fixtures until PRD finals.

#### 12. Admin Stakers table UI
- [ ] Masked address + full on hover/click (pattern как в продукте).
- [ ] Sort indicators на headers.
- [ ] Status Active/Restricted visually distinct.
- [ ] Pagination controls; empty/loading states.
- [ ] Row → detail без потери контекста (предпочтительно route `/admin/wallets/<address>` — CONTEXT).

---

### B-P2 — polish / consistency

#### 13. Тикер vs полное имя
- [ ] Amount contexts: **MEX**; brand/hero: MEXICO OK; whitepaper «TOKENS» dual label fix (365 vs 70%).

#### 14. Empty-state copy variants
- [ ] Personal dashboard vs Admin Wallet Lookup — разные формулировки, не один generic.

#### 15. Android MWA
- [ ] Phantom/Solflare connect на Android: «We could not reach Mobile Wallet Adapter» — баг открыт; iOS TBD.
- [ ] Desktop adapters не регрессируют.

#### 16. Decorative / thematic
- [ ] Кактусы, confetti, splash — не перекрывают кликабельные CTA (hitbox).
- [ ] Reduced motion preference (желательно): уменьшить ambient loops.

---

### B-P3 — ждёт дизайн / внешнее

- [ ] Final Mexican theming assets (sombrero icon, colors) — note в Web Frontend.
- [ ] FigJam boards: сверить pixel-level после стабилизации логики  
  (`design-dark-dao` landing / modals nodes из тикетов).
- [ ] Token Price card UI когда появится 3rd-party feed.

---

## Сводная матрица тикет → приоритет

| Тикет | Функционал | UI |
|---|---|---|
| Claim / Compound / Unstake | **A-P0** | B-P0 (amounts, unlock affordance) |
| Staking (Deposit) | **A-P0** | B-P0 / B-P1 (confirm modal) |
| Daily Check-in & Reward Rate | **A-P0** | B-P0 (cells), B-P1 (modal) |
| Mainnet deploy runbook | **A-P0** | — |
| Self-Hosted Indexer | **A-P0** | косвенно (данные UI) |
| Missing Tokenomics limits | **A-P0 decision** | occupancy UI после PO |
| Web Frontend + Landing (logic) | **A-P1** | **B-P1** |
| My Positions + History | **A-P1** | **B-P1** |
| Staking Action Modals | **A-P1** | **B-P1** |
| Modal progressive load / check-in / unstake missing | **A-P1** | **B-P0** |
| Audio Feedback | **A-P1** | **B-P1** |
| Admin Config refactor | **A-P1** | **B-P1** |
| Empty State (connected, no positions) | **A-P1** | **B-P0** |
| Admin Stakers table | **A-P1** | **B-P1** |
| Intro splash animation | **A-P2** | **B-P1** (perf + sequence) |
| Android MWA / ticker polish | — | **B-P2** |
| Final visual assets / FigJam pixel QA | — | **B-P3** |

---

## Рекомендуемый порядок прогона (практика)

1. **A-P0 money path** на devnet: stake → check-in → claim → unlock → auto-compound → manual compound → unstake (+ pause/restriction/empty pool).  
2. **Indexer lag & history** на тех же tx.  
3. **Mainnet runbook rehearsal** на devnet (особенно step 9).  
4. **A-P1 dashboard/modals/empty/audio/admin config payloads.**  
5. **B-P0 money-display bugs** (rounding, empty-state copy, 7 vs 10 days).  
6. **B-P1 landing + splash + mobile adaptive.**  
7. **PO gate** по caps → затем occupancy + cap enforcement.  
8. **B-P2/P3 polish** и pixel-pass по FigJam.

---

## Связь с уже известными багами (CONTEXT)

| Известное | Куда класть в прогоне |
|---|---|
| BUG-001 Helius API key на фронте | A-P0 mainnet prep + Web Frontend security smoke |
| UI rounding (1500.1999 → 1,500.20 vs 1,500.19) | **B-P0 #1** |
| CFG-08 per-wallet cap vs pool total | A-P0 Tokenomics + Admin Config |
| Reward Vault withdraw → multisig ATA, не личный wallet | Admin money path / Squads QA |
| Compound enforcement в lock (спека явно для unstake, не для compound) | A-P0 Claim/Compound — уточнить у команды |
| Android MWA | B-P2 |
| Design bugs: empty-state copy; 10→7 days; check-in modal while disconnected | B-P0 / B-P1 |
