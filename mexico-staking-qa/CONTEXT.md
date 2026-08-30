# Mexico Staking (MEX) — полный контекст QA-проекта

Документ агрегирует весь контекст, накопленный в переписке по проекту, чтобы
им можно было пользоваться как единой точкой входа (для Ники или для
следующего агента/тестировщика), не поднимая исходный чат заново.

Обновлено: 30 августа 2026.  
См. также `PRIORITY_TEST_PLAN.md` — приоритизация проверок по тикетам
(функционал / UI, P0–P3).

---

## 1. Проект и окружение

- **Проект:** MEXICO (тикер **MEX**) — стейкинг-платформа на Solana.
- **Окружение тестирования:** devnet.
- **Фронт (user):** `mexicoweb-dev.up.railway.app`.
- **Админка:** `dark-dao-admin.up.railway.app` (разделы: Dashboard,
  Configuration Management, Reward Vault, Wallet Lookup).
- **Ответственный за тестирование:** Ника (проект назначен ей).
- **Репозиторий с QA-артефактами:** `Mykola-Ursal/New_rep` (этот репозиторий).
  Корневой `README.md` относится к другому, не связанному проекту
  (авторизация/2FA/whitelist) — не трогали.
- **Ветка с QA-пакетом:** `cursor/mexico-staking-qa-consolidation-7afc`
  (база — `main`).
- **PR:** [#2 — Mexico Staking (MEX) QA: consolidated Excel checklist + formal bug reports](https://github.com/Mykola-Ursal/New_rep/pull/2)
  (draft, open, актуален на момент этого документа).

## 2. Исходное ТЗ (что было в самом начале)

В начале был вставлен полный пакет тикетов PRD по проекту:

- **Токеномика с нерешёнными лимитами** — три параметра явно помечены в PRD
  как решения, которые должен принять продукт-оунер, и **ни один из них
  сейчас не реализован/не проверяется** в коде:
  - глобальный кап стейкинга — **30 000 000 MEX**;
  - кап на кошелёк — **500 000 MEX**;
  - индикатор занятости пула (pool occupancy indicator).
- **Токен MEX** — фиксированный саплай **1 000 000 000**, mint authority
  отключён после создания.
- **Флоу стейкинга** — независимые позиции без лимита на их количество на
  кошелёк.
- **Daily check-in** — прогрессия ставки по тирам: `primary 5–10%`,
  `secondary 2.5–5%`.
- **Claim / Compound / Unstake** — с автокомпаундом при анлоке позиции.
- **Админка** — мультисиг **Squads**.
- **Инфраструктура** — devnet-деплой, индексер, read-only API.

### Практические вопросы по окружению (обсуждались отдельно)

- Публичного крана MEX на devnet нет **по дизайну** — тестовые токены нужно
  получать переводом с dev-кошелька команды либо через отдельный
  mint-скрипт.
- Невидимый токен в Phantom добавляется либо тумблером в списке скрытых
  токенов, либо поиском/добавлением вручную по адресу минта.

## 3. Что было сделано командой ДО подключения агента

Собраны и уже отправлены (файлами в чате, не в репозитории) три чек-листа в
формате CSV (`Title;How to test;Expected Result`):

| Файл (оригинал, только в чате) | Кейсов | Покрытие |
|---|---|---|
| `mexico_smoke_fast.csv` | 25 | Линейный прогон одним кошельком: от установки минимального лока до анстейка — рассчитан на один вечер |
| `mexico_break_it_tonight.csv` | 28 | Обход авторизации, IDOR, race conditions, обход клиентской валидации — всё через DevTools + Phantom, без Anchor/CLI |
| `mexico_solana_specific.csv` | 24 | Специфика сети: rent, ATA, compute budget при множестве позиций, подмена PDA-аккаунтов, on-chain Clock против системных часов, replay транзакций, порог подписей мультисига |

### Находки по скриншотам (не из чек-листов, вытащены из Network tab)

1. **Утечка Helius API-ключа.** Ключ провайдера передаётся в открытом виде в
   query-параметре каждого RPC-запроса с фронта (`?api-key=...`). Любой
   человек может скопировать его из DevTools. Риск: посадка квоты, а если
   ключ платный/общий с продакшеном — проблема на mainnet. Предложенное
   решение: RPC должен идти через собственный бэкенд-прокси, а не напрямую с
   фронта.
2. **Подозрение на проблему округления claim'ов.** В истории операций видны
   дробные claim'ы вида `+0.001` и `+0.005` в один день. Сигнал для проверки:
   не даёт ли частый клейм суммарно больше, чем начислено по формуле, и не
   теряются ли начисления на клейме, который округляется до нуля.

### Ключевой принцип тестирования контрактов (сквозная идея всего проекта)

На Solana **фронт — это подсказки для честного пользователя, а не защита**.
Программа (смарт-контракт) — единственный источник правды, данные лежат в
отдельных аккаунтах. Поэтому для каждого действия имеет смысл проверять
одно и то же **дважды**:

1. **Через интерфейс** — должна ли кнопка/форма блокировать действие.
2. **В обход интерфейса** — через прямой запрос/инструкцию, скопированную из
   Network tab, — должна ли сама программа отклонить его на уровне
   валидации аккаунтов/инструкции.

Если фронт блокирует, а программа — нет, это баг.

Дополнительно проговорено:

- Транзакция на Solana — **всё или ничего** (атомарность).
- Платить приходится **и за комиссию, и за rent** на новые аккаунты — в том
  числе при неуспешных транзакциях комиссия всё равно списывается.
- Время лока и check-in дней должно браться из **on-chain Clock**, а не с
  устройства пользователя.

### Что было явно не сделано на момент передачи агенту

- Три CSV не сведены в один Excel с вкладками + колонкой статус/приоритет
  (было предложено, но не запрошено).
- Формальные баг-репорты по утечке Helius-ключа и по округлению claim'ов не
  оформлены отдельными документами — только описаны в чате.

## 4. Что сделал агент (хронология по итерациям)

### Итерация 1 — консолидация чек-листов + баг-репорты

1. Проверил репозиторий: он оказался фактически пустым (только несвязанный
   `README.md` от другого проекта). Оригинальные три CSV из чата в
   репозитории отсутствовали.
2. Создал ветку `cursor/mexico-staking-qa-consolidation-7afc`.
3. Так как оригинальные CSV физически недоступны агенту (существовали
   только как вложения в чате), **реконструировал их содержимое** по
   подробным описаниям охвата/тематики из саммари, сохранив те же названия
   файлов и то же количество кейсов (25 / 28 / 24), плюс общую доменную
   специфику Solana-стейкинга. Это явно помечено как допущение в
   `README.md` пакета — до реального прогона нужно сверить с оригиналами,
   если они сохранились у Ники.
4. Создал каталог `mexico-staking-qa/` со следующими файлами:
   - `README.md` — контекст проекта, принципы тестирования, открытые
     вопросы.
   - `csv/mexico_smoke_fast.csv` (25 кейсов).
   - `csv/mexico_break_it_tonight.csv` (28 кейсов).
   - `csv/mexico_solana_specific.csv` (24 кейса).
   - `scripts/build_master_workbook.py` — Python-скрипт на `openpyxl`,
     собирающий CSV в единый `.xlsx`.
   - `Mexico_Staking_QA_Master.xlsx` — сгенерированный мастер-файл: по
     вкладке на чек-лист + вкладка `Summary` с формулами `COUNTIF` по
     статусам; в каждой вкладке добавлены выпадающие (data validation)
     колонки `Status` (`Not tested / Passed / Failed / Blocked / Skipped`)
     и `Priority` (`P0–P3`).
   - `bug_reports/BUG-001-helius-api-key-exposed.md` — формальный
     баг-репорт: severity Critical, шаги воспроизведения, impact
     (истощение квоты, риск на mainnet при переиспользовании ключа),
     рекомендация (бэкенд-прокси для RPC).
   - `bug_reports/BUG-002-claim-rounding-dust.md` — формальный
     баг-репорт-расследование: severity Medium (pending verification), два
     возможных failure mode (переплата при частых мелких клеймах vs потеря
     accrual при округлении до нуля), шаги для подтверждения.
5. Закоммитил, запушил, создал **PR #2** (draft) с подробным описанием на
   русском, включая явную оговорку про реконструкцию контента.

### Итерация 2 — глубокий тест-план по unstake

Пользователь спросил, какой следующий шаг, и сам предложил разобрать
`unstake`. Агент согласился (unstake — точка вывода средств, где
пересекаются lock-логика, rent, автокомпаунд и потенциальный IDOR) и:

1. Создал `csv/mexico_unstake_deep_dive.csv` — **37 кейсов** с
   дополнительной колонкой `Category` (в отличие от трёх исходных
   чек-листов, где только `Title;How to test;Expected Result`).
   Категории и количество кейсов:
   - Happy path — 3
   - Timing / lock — 4
   - Validation — 4
   - Security / IDOR — 6
   - Race condition — 3
   - Solana mechanics — 3
   - Rent / accounts — 3
   - Multisig / admin — 2
   - Rewards interaction — 3
   - UI/UX — 6
2. Обобщил `scripts/build_master_workbook.py`: раньше схема колонок была
   жёстко зашита (`Title, How to test, Expected Result`), теперь скрипт
   динамически читает заголовки каждого CSV, что позволило корректно
   отрисовать колонку `Category` только в unstake-вкладке, не ломая
   остальные три.
3. Пересобрал `Mexico_Staking_QA_Master.xlsx` — теперь **4 вкладки**
   чек-листов (`Smoke Fast`, `Break It Tonight`, `Solana Specific`,
   `Unstake Deep Dive`) + `Summary`; всего **114 кейсов** в мастер-файле.
   В `Summary` добавлена пометка, что `Unstake Deep Dive` пересекается с
   unstake-кейсами внутри остальных трёх чек-листов и должен считаться
   авторитетным расширенным источником по unstake (чтобы не задваивать
   кейсы при подсчёте общего покрытия).
4. Обновил `README.md`: добавил описание нового файла и пункт «следующий
   приоритет» — прогнать `mexico_unstake_deep_dive.csv`.
5. Закоммитил, запушил, обновил описание **PR #2**.

### Итерация 3 — CONTEXT.md + разбор вывода из Reward Vault

1. По запросу «собери максимальный контекст из чата» собран этот документ
   (`CONTEXT.md`) как единая точка входа.
2. Разобрана успешная on-chain транзакция вывода ~9 999 992.36 MEX из
   Reward Vault через админку (см. §8 ниже): токены уходят **не на личный
   кошелёк**, а в token account казны мультисига Squads.

## 5. Поздняя сессия QA (саммари, ~26–30 августа 2026)

Ниже — контекст отдельной (более поздней) сессии по тому же проекту. Её
артефакты (полный тест-план на 579 кейсов, аудит, UI-баги) в основном
существовали как файлы в чате и **пока не продублированы** в этот
репозиторий.

### 5.1. Аудиты и отчёты (mexico-token / SDK)

Разобран security/fintech-аудит (Shutiak, mexico-token, 26.08.2026) по
SDK/deploy-скриптам:

- **2 HIGH**
  - Неиспользуемый `@anchor-lang/core` на машине с mint authority key.
  - Гонка между созданием mint и записью в реестр — риск второго токена на
    mainnet.
- **5 MEDIUM**
  - Silent u64 wrap в `u64le`.
  - Squads-декодер прячет signer/writable флаги.
  - Metadata update authority не сверяется с Squads vault PDA.
  - Per-wallet cap сверяется с pool-wide total вместо стейка кошелька.
  - Ссылка на Squads-дашборд без валидации URL.

Сопоставление с ручным тест-планом:

- Находка про update authority уже была поймана раньше
  (`mexico_token_checklist`, п. 33/34).
- Находка про per-wallet cap **независимо подтверждена на контракте**
  кейсом CFG-08 (`lib.rs:441-446`) — закрыла пометку аудитора
  «unverified».

Структурный вывод по покрытию:

| Слой | Кто покрывает |
|---|---|
| Rust-контракт (программа) | Наш тест-план / Rust-харнес |
| TypeScript-слой (SDK / deploy-скрипты) | Аудит Shutiak |
| `apps/*` (фронт / API) | **Не покрыт ни там, ни там** |

### 5.2. Перевод и оформление полного тест-плана (579 кейсов)

- Перевели тест-план по стейкингу (**579 тест-кейсов**) с русского на
  английский: разбили на 7 чанков по разделам → параллельный перевод →
  merge; порядок 1:1 с оригиналом, без потерь и без остатков кириллицы.
- Финальный `.xlsx` с **17 табами** по разделам (`stake`, `unstake`,
  `claim`, `compound`, `check_in`, `update_config`, …) + лист `Contents`
  с навигацией и счётчиками.
- Убрали ID из Title (ID остался только в своей колонке).
- Переписали Expected results в формате профессиональных проверяемых
  утверждений: точные коды ошибок, негативные проверки («что не должно
  измениться»), без филлера вроде «Succeeds.» / «Works correctly»; там,
  где реальный прогон разошёлся с исходным ожиданием, expected result
  отражает **фактически проверенное** поведение.
- Пронумеровали пункты (вместо буллетов) и починили высоту строк
  (симуляция переноса текста + проверка рендером).

Файлы сессии (отправлены в чат, в этот репозиторий пока не лежат):

- `mexico_staking_testcases_en.csv` — перевод, 579 строк
- `mexico_staking_testcases_en.xlsx` — финальная версия с табами
- `mexico_master_checklist.csv` — сводный чек-лист по всем фичам

> Ранние реконструированные CSV в `mexico-staking-qa/csv/` (smoke / break
> it / solana / unstake deep dive, ~114 кейсов) — **черновой пакет** из
> первого саммари. Авторитетный полный тест-план — **579-кейсовый**
> `mexico_staking_testcases_en.xlsx` из этой сессии.

### 5.3. UI/UX ревью и баги (`mexicoweb-dev`)

**Тикер vs полное имя.** На экране стейкинга разнобой: где-то «MEX»,
где-то «MEXICO»; в поле ввода суммы — только иконка, без текстового
обозначения токена. Рекомендация: унифицировать на **тикер MEX** везде.

**Округление сумм MEX — крупнейшая UI-находка сессии.**

- On-chain (Explorer): всегда двигается точное сырое значение
  (пример: `1500.1999`), без округления при списании/зачислении.
- Модалка подтверждения показывала `1,500.20` (round **up**).
- Success / таблица позиций — `1,500.19` (round **down**).
- Total Staked считался от округлённого вверх числа → не сходился даже с
  суммой строк таблицы позиций (`3,000.26` vs фактических `3,000.25`).
- Рекомендация: раз округление ничего не защищает (реальная сумма всегда
  точная), округление должно быть **вниз (truncate) везде без
  исключений** — модалка, Success, таблица позиций, Total Staked.

Это закрывает/уточняет ранний `BUG-002` (dust/rounding на claim): проблема
не только в dust-клеймах, а в **несогласованном отображении** точных
on-chain сумм на всём UI.

**Wallet Lookup / админка.** Как встроить таблицу стейкеров без потери
контекста: рекомендован отдельный роут `/admin/wallets/<address>` вместо
модалки/инлайн-блока — внутри detail-вью есть реальные admin-действия
(block principal / reward withdrawal).

**Configuration Management — смысл метрик:**

- TVL display deviation / interval — политика «устаревания» отображаемого
  TVL.
- Reward pool warning / critical thresholds — алерты на остаток резерва
  под уже начисленные награды.
- Global / per-wallet stake cap — сырые base units (риск опечатки на
  порядок при вводе).

**Wallet connection на Android.** MWA (Mobile Wallet Adapter) падает с
ошибкой «We could not reach Mobile Wallet Adapter» при подключении
Phantom/Solflare. Баг-репорт оформлен; на iOS воспроизведение не
подтверждено.

**Compound vs lock.**

- Claim доступен всегда, даже в lock.
- Manual compound недоступен в lock; автокомпаунд при анлоке — один раз.
- Спека явно прописывает контрактный enforcement для unstake
  («independently of the interface»), но **не для compound** — открытый
  вопрос к команде.

**Мелкие находки.**

- Дубль лейбла «TOKENS» в whitepaper (365 vs 70% — разные метрики под
  одинаковой подписью).
- Paste bypass validation ведущих нулей в поле суммы.
- Empty-state тексты («No open positions…») — формулировка под разный
  контекст: личный дашборд vs админский Wallet Lookup.

### 5.4. Грамматика и оформление баг-репортов

Правки английского и структуры: пропущенные Actual result / Steps to
Reproduce; «Tested,» → «Tested:»; «approve is asked by» → нормальный
английский; «needs the additional fixing» → «needs additional fixing»;
«флажками» → «bunting/flag banner»; разделение Actual/Expected там, где
формулировки были перепутаны местами.

## 6. Разбор вывода из Reward Vault (админка → Explorer)

Контекст: пользователь вывел ~9 999 992.36 MEX из Reward Vault через
`dark-dao-admin.up.railway.app/admin/vault` и не находил эту сумму на
Explorer по своему кошельку.

**Транзакция (devnet):**  
`4oVakwKit3XJBax6AwwmupkwX3xcSwBSPMtMMPdnU9SZvp87mQMckGv58d7Gto67EB6uid6mWRjdvbU8ED3qUj1c`  
Status: Success / Finalized. Fee payer (один из подписантов мультисига):
`4amNLu1hAJWWyLDeZ1u7sUuaE5wKuycBshKCsgTBAKLU`.

**Что произошло on-chain:**

1. Squads Multisig `VaultTransactionExecute` исполнил одобренное
   предложение (multisig
   `FJDCDK55K3TCEbicbJbumI5doAlGFEvTIIMX3zff33BE`).
2. Inner: `Staking: Withdraw Vault` → `Token Program: Transfer (Checked)`.
3. Source (Reward Vault ATA):
   `8U5pDdtuuFg5gHD2wKWNsfQmgAwTMVoP2SjHktEd83kE`
   (−9 999 992.36 MEX → post ~20 000 000.00 — совпадает с UI «Current
   balance» после вывода).
4. Destination:
   `61GHKKeT1oGwaReg1MKtx1Fup1SE2Ft7kHfKRQwbcx3Z`
   (+9 999 992.36 MEX). Owner этого ATA —
   `9hbYfQcyilNF1bg548rVRmqktpzu4XwPFYEQEwLJohWh` — **казны/authority
   мультисига**, не личный Phantom.

MEX имеет **9 decimals**: в поле админки «Amount to withdraw» вводится
сырое число `9999992360000000` (= 9 999 992.36 × 10⁹).

**Почему сумма «не находится» на Explorer:** вывод из Reward Vault
переводит токены **в token account казны мультисига**, а не на личный
кошелёк подписанта (`4amNLu…` / `4YDT…CfA7`). Чтобы увидеть сумму — искать
по `61GHKKeT1oGwaReg1MKtx1Fup1SE2Ft7kHfKRQwbcx3Z` (или owner
`9hbYfQcy…`). Перевод на личный кошелёк — отдельный Squads-proposal из
казны мультисига.

**Побочный риск:** на UI после успешного вывода всё ещё висела плашка
«Change 41 — 0 of 2 signatures collected». Либо устаревший кэш админки,
либо **второе, ещё не исполненное предложение** на ту же сумму — нужно
проверить в Squads и при дубликате отменить (Cancel), иначе возможен
повторный вывод ~10M MEX.

## 7. Текущее состояние репозитория (файлы в `mexico-staking-qa/`)

```
mexico-staking-qa/
├── README.md                                   # ранний контекст / принципы
├── CONTEXT.md                                   # этот документ (полный контекст)
├── Mexico_Staking_QA_Master.xlsx                # ранний пакет: 4 вкладки, ~114 кейсов
├── csv/
│   ├── mexico_smoke_fast.csv                    # 25 (реконструкция)
│   ├── mexico_break_it_tonight.csv              # 28 (реконструкция)
│   ├── mexico_solana_specific.csv               # 24 (реконструкция)
│   └── mexico_unstake_deep_dive.csv             # 37, с Category
├── scripts/
│   └── build_master_workbook.py                 # генератор .xlsx из CSV
└── bug_reports/
    ├── BUG-001-helius-api-key-exposed.md        # Critical
    └── BUG-002-claim-rounding-dust.md           # уточнён UI-rounding из §5.3
```

**Не в репозитории (только в чате / у команды):** полный
`mexico_staking_testcases_en.xlsx` (579 кейсов, 17 табов),
`mexico_master_checklist.csv`, отчёт аудита Shutiak, UI-баг-репорты
(Android MWA, округление UI, тикер/MEXICO и т.д.).

**Git:** ветка `cursor/mexico-staking-qa-consolidation-7afc`, коммиты
поверх `main` включают пакет smoke/break/solana/unstake + CONTEXT.md.

**PR:** [#2](https://github.com/Mykola-Ursal/New_rep/pull/2), статус
`OPEN`, `draft`, база `main`.

## 8. Открытые вопросы / что осталось сделать

### Продукт / спека

- [ ] Продукт-оунер: лимиты токеномики (global 30M, per-wallet 500k,
      occupancy indicator) — и когда они реально enforced on-chain.
- [ ] Уточнить у команды: для **manual compound** нужен ли контрактный
      enforcement независимо от UI (как явно прописано для unstake), или
      достаточно UI-блокировки в lock.

### Контракт / аудит

- [ ] Закрыть HIGH-пункты аудита (mint race, unused `@anchor-lang/core` на
      машине с mint key) до mainnet.
- [ ] Per-wallet cap: починить сверку со стейком кошелька, а не с
      pool-wide total (CFG-08 / MEDIUM аудита).
- [ ] Metadata update authority ↔ Squads vault PDA.

### UI / фронт (`apps/*` — пока без покрытия тестами)

- [ ] Унифицировать отображение токена на **тикер MEX**.
- [ ] Округление UI: truncate вниз везде (модалка / Success / позиции /
      Total Staked).
- [ ] Android MWA: «We could not reach Mobile Wallet Adapter».
- [ ] Wallet Lookup: роут `/admin/wallets/<address>` вместо модалки.
- [ ] BUG-001: Helius API key не должен уходить с фронта в query-param.
- [ ] Проверить «Change 41» в Squads после вывода из Reward Vault
      (дубликат proposal vs stale UI).

### QA-артефакты в этом репозитории

- [ ] Залить в репо авторитетный `mexico_staking_testcases_en.xlsx`
      (579 кейсов) — сейчас здесь только ранний ~114-кейсовый пакет.
- [ ] Довести BUG-001 / BUG-002 пруфами (HAR, Explorer screenshots,
      signature ссылки).
- [ ] Решить, переводить ли PR #2 из draft в ready.

## 9. Быстрые ссылки

- PR: <https://github.com/Mykola-Ursal/New_rep/pull/2>
- Ветка: `cursor/mexico-staking-qa-consolidation-7afc`
- User UI: `mexicoweb-dev.up.railway.app`
- Admin UI: `dark-dao-admin.up.railway.app`
- Пример withdraw tx (devnet):
  <https://explorer.solana.com/tx/4oVakwKit3XJBax6AwwmupkwX3xcSwBSPMtMMPdnU9SZvp87mQMckGv58d7Gto67EB6uid6mWRjdvbU8ED3qUj1c?cluster=devnet>
- Multisig (Squads): `FJDCDK55K3TCEbicbJbumI5doAlGFEvTIIMX3zff33BE`
- Multisig MEX ATA (куда уходит withdraw):
  `61GHKKeT1oGwaReg1MKtx1Fup1SE2Ft7kHfKRQwbcx3Z`
- Reward Vault ATA: `8U5pDdtuuFg5gHD2wKWNsfQmgAwTMVoP2SjHktEd83kE`
- Скрипт пересборки раннего xlsx:
  `python3 mexico-staking-qa/scripts/build_master_workbook.py`
  (из каталога `mexico-staking-qa/`, нужен `openpyxl`)
