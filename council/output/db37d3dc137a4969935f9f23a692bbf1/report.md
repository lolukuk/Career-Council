# Отчёт совета пяти персон

Статус: **no_consensus**

peter_thiel:object; peter_thiel:new obligation; peter_thiel:unmet criterion; warren_buffett:object; warren_buffett:new obligation; warren_buffett:unmet criterion; robert_reich:object; robert_reich:unmet criterion; nassim_nicholas_taleb:object; nassim_nicholas_taleb:new obligation; nassim_nicholas_taleb:unmet criterion; marcus_aurelius:object; marcus_aurelius:unmet criterion

Режим: `model`. Режим выбранного LLM-провайдера. Формальное согласие не доказывает качество решения.

Вопрос: I'm thinking about switching careers from mechanical engineering to software development. Help me think through this decision.

Человек принимает итоговое решение после отчёта. Его выбор не меняет статус согласия персон.

Условный тестовый режим AI Tunnel. Превышения запрошенного лимита допускаются только до отдельного жёсткого потолка; этот профиль не предназначен для production.
Запрошено: 2000 токенов; потолок приёма: 8000; полученных ответов с превышением: 0.

Провайдер: `aitunnel`; модель: `gpt-6-luna-pro`; учёт контекста: `server_enforced`.

Reasoning effort: `none`. Эта настройка влияет на расход и качество модели; none используется для проверки процесса.

Предварительный count OpenAI ограничивает бюджет приложения, не подтверждает окно любой модели. AI Tunnel проверяет переполнение на сервере без точного предварительного count; сжатие отключено.

Лимит попыток относится к локальным запросам. Внутренние повторы провайдера и расходы после отмены неизвестны. Usage полученных ответов, включая отклонённые, сохранён в trace; отсутствующие данные не означают нулевой расход.

## Рекомендация и план

Stay employed while testing software through a polished domain-relevant project and realistic work exposure. Revisit training or a switch only after Lisa agrees to specific household limits and actual figures support a stopping rule; do not assume hiring or salary outcomes.

Шаги:

1. With Lisa, agree on childcare limits, budget, minimum savings/income floor, and a dated stopping rule before any costly transition.
2. Build and deploy one useful automotive/mechanical software project while employed; seek feedback and test whether the work suits you.
3. Review evidence and household numbers together before considering part-time training, bootcamp, or leaving work; treat outcomes as uncertain.

Альтернативы:

- Stay employed while running a bounded software-fit and market test.
- Consider part-time training only after family and financial guardrails are agreed.
- Defer quitting or full-time bootcamp until evidence and safeguards clear.

## Риски и условия решения

- Whether Mark enjoys software as paid work, can secure a role, and what salary/timeline are achievable remain unknown; portfolio or study progress alone does not establish these.
- Lisa's buy-in, household cash flow, childcare capacity, savings floor, and stopping rule are not established; do not treat the transition as cleared without agreement and actual figures.
- Study pace, burnout, bootcamp effectiveness, and future earnings are uncertain; avoid treating any path or outcome as guaranteed.

Версия 1, digest `4e39fca17618f58aa025a23a54ea034998b14b22a947624b29f1460e3701f3cb`. Полный неизменный JSON решения сохранён в trace.json.

## Общий итог после обсуждения

Обсуждение завершено после 1 из 1 разрешённых раундов. Единогласного одобрения нет. План выше остаётся предложением с условиями; возражения ниже входят в итог и не считаются устранёнными.

Оценки общего проекта и основания разногласий:

- Peter Thiel — object: Supported: proposal preserves income and names household safeguards. Unsupported as established outcomes: none claimed; project value and fit remain explicitly uncertain.
  Условие peter_thiel/c1 не выполнено: Unmet: no shipped project or market feedback; Lisa's buy-in and financial rule are not established.
  Утверждение v1/guard / qualified: Risk is evidenced, but actual affordability and family agreement remain unknown.
  Утверждение v1/slow / qualified: Slow study and project idea are supported; project's signaling value is not guaranteed.
  Утверждение v1/fit / qualified: Plausible experiment, but no evidence yet of job fit or market response.
- Warren Buffett — object: Supported overall; no unsupported source assertions identified. Assumptions are caveated. Still, the blocking decision criterion is unmet.
  Условие warren_buffett/c1 не выполнено: Unmet: actual cash flow, salary floor, Lisa’s buy-in, and work-fit evidence are not established.
  Утверждение v1/guard / qualified: The downside is supported; actual cash flow and safeguards remain unknown.
  Утверждение v1/slow / qualified: Scattered study and project idea are documented; polished-project value is not proven.
  Утверждение v1/fit / qualified: A bounded test is a recommendation, not evidence it predicts hiring or paid-work fit.
- Robert Reich — object: Supported overall as a cautious experiment, but the blocking criterion is unmet. Strongest counterargument: scarce study time risks delay and burnout; actual employer offers and family costs remain unknown.
  Условие robert_reich/c1 не выполнено: Unmet: Lisa's buy-in, paid-work fit, income floor, and stopping rule are prerequisites, not established.
  Утверждение v1/guard / qualified: Savings and income-risk claim is supported; exact household impact still needs actual figures.
  Утверждение v1/slow / qualified: Notes support scarce study time and possible burnout, not that the proposed project tests market demand.
  Утверждение v1/fit / qualified: Reasonable assumption, explicitly caveated; work exposure alone cannot prove hiring or earnings.
- Nassim Nicholas Taleb — object: Supported as cautious, reversible advice, with caveats; future hiring, earnings, and project outcomes are not established.
  Условие nassim_nicholas_taleb/c1 не выполнено: Criterion is unmet: multiple safeguards and fit/traction evidence are explicitly missing.
  Утверждение v1/guard / qualified: Evidence supports material downside, not a quantified loss; household figures remain unknown.
  Утверждение v1/slow / qualified: Scattered study and project idea are evidenced; project value or market response is not guaranteed.
  Утверждение v1/fit / qualified: Assumption is a testable rationale, not evidence of hiring or fit.
- Marcus Aurelius — object: Recommendation is cautious and evidence-aligned, but its blocking family-and-fit gate remains unmet; defer approval of any switch.
  Условие marcus_aurelius/c1 не выполнено: Unmet: genuine buy-in, tested runway and software-work aim are not established.
  Утверждение v1/guard / qualified: Evidence supports substantial downside risk, not a precise loss forecast.
  Утверждение v1/slow / qualified: Scattered study is documented; project value and burnout remain uncertain.
  Утверждение v1/fit / qualified: A test may provide information, but does not establish fit or hiring.

## Пять позиций и текущие оценки

### Peter Thiel

Build a domain-specific software project while employed; test demand before choosing bootcamp or leaving engineering.

Аргументы этого взгляда:

- Your edge isn’t a credential: it’s building software for physical engineering problems.
- Quitting for bootcamp puts savings at risk; first tech pay may also trail your current salary.

Критерии:

- Switch only after a shipped, domain-specific project and real market feedback; get Lisa’s genuine buy-in and set a financial stopping rule before any costly leap.
Контраргумент: Six scattered study hours weekly could stretch the path dangerously; delay is not risk-free. But an untested bootcamp bet is worse.

Оценка: **object** — Object: credentials are no moat; domain expertise may differentiate, but the proposal has not yet met its own shipped-project/market-feedback gate. Strong counterargument: delay risks burnout.

No prior vote is recorded; I assessed this version independently against the stated edge and decision gate.

### Warren Buffett

Stay employed while testing software and building a domain-based portfolio; defer quitting or tuition until the decision gate is met.

Аргументы этого взгляда:

- Protect the downside: a full-time bootcamp could consume much of savings while income falls.
- Software offers a plausible domain-specific edge, but scarce study time makes self-study slow and burnout-prone.

Критерии:

- Choose a reversible path only after real cash-flow and salary-floor numbers, Lisa’s genuine buy-in, and evidence Mark wants software work—not merely escape from boredom.
Контраргумент: Waiting is not free: scarce evening hours may stretch self-study for years, while a focused bootcamp could accelerate a domain-specific transition.

Оценка: **object** — Circle of competence and margin of safety favor a reversible test, not a bootcamp leap. Strongest counterargument: scarce study time may prolong burnout; acceleration remains uncertain.

No draft changes to assess; review the immutable version 1 proposal against the evidence and my criterion.

### Robert Reich

Test a low-risk transition while employed; use a domain-led portfolio and network before considering a costly leap.

Аргументы этого взгляда:

- Protect income: a full-time bootcamp could consume much of the $42k savings.
- Part-time study is slow, and coding-as-work remains untested.

Критерии:

- Choose only after Lisa's genuine buy-in, testing paid-work fit, and setting a household income floor and savings/job-search stopping rule.
Контраргумент: Slow study can prolong burnout; a focused bootcamp may accelerate entry, but employer offers—not promises—must justify the family risk.

Оценка: **object** — Object: proposal sensibly protects income, but its own stated decision gate is not met. Lisa bears added childcare costs; no employer offer, pay, benefits, or hiring timeline is established.

No proposal changes are authorized in review; assessed the exact submitted version.

### Nassim Nicholas Taleb

Run a bounded experiment while employed; don't quit or buy the bootcamp until safeguards and evidence clear the criterion.

Аргументы этого взгляда:

- Protect income and savings; quitting for bootcamp puts a thin cushion under a costly, uncertain transition.
- Test software work with a polished domain project and realistic exposure; slow study also risks burnout and may not test job fit.

Критерии:

- Switch only after Lisa's genuine buy-in, real cash-flow and salary-floor limits, a stopping rule, and evidence of job-fit and hiring traction; keep downside reversible.
Контраргумент: Self-study is scarce and burnout-prone; delay may prolong dissatisfaction, while domain expertise could differentiate you. A bootcamp may accelerate progress, but outcomes remain uncertain.

Оценка: **object** — Approve the employed experiment, not a career switch: it limits downside while testing fit. Counterpoint: slow study risks burnout; bootcamp acceleration is unproven.

No prior draft: the bounded, employed test preserves optionality; the strongest counterargument is scarce study time and burnout, while bootcamp speed and hiring outcomes remain unproven.

### Marcus Aurelius

Keep your job while testing software with a shipped domain-relevant project; defer bootcamp or quitting until family guardrails are real.

Аргументы этого взгляда:

- Build toward software without quitting: keep income, protect family time, and test the work in a small daily practice.
- Part-time study is scarce and slow, but engineering domain knowledge may differentiate you.

Критерии:

- Before an irreversible switch, confirm Lisa's genuine buy-in, a household-tested runway/stopping rule, and that software work—not merely escape from current work—is the aim.
Контраргумент: Six hours of scattered study may drag on and risk burnout; a structured bootcamp could accelerate progress, but its timeline and hiring outcome are uncertain.

Оценка: **object** — The bounded test is prudent; strongest counterargument is slow study and burnout. Keep a sustainable practice, but family duty requires actual consent and guardrails before transition.

No draft changes to assess; the proposed bounded test preserves income while deferring costly commitments pending evidence and family agreement.

## Возражения и противоречия

- o1 / Peter Thiel: The unfair advantage may be engineering-domain insight applied to software for physical products—not generic junior coding or a credential. But this is a thesis, not demonstrated demand; test it with a shipped project and buyer/employer feedback before treating it as an edge. (pending).
- o2 / Warren Buffett: I support the employed experiment, but criterion warren_buffett/c1 is unmet: neither actual household cash-flow/salary-floor figures and Lisa's genuine buy-in nor evidence of paid-work fit is established. Do not treat a costly transition as cleared. (pending).
- o3 / Nassim Nicholas Taleb: The proposal appropriately defers quitting, but do not infer affordability or a safe stopping rule: household spending, cash floor, and Lisa's agreement are unknown. (pending).

## Недостающие данные

- Household spending and safe cash floor.
- Lisa’s explicit buy-in and agreed stopping rule.
- Evidence of software-job fit and local hiring response.
- Six-month household cash flow and acceptable salary floor
- Lisa’s explicit agreement and workable family plan
- Evidence of fit with software work
- Lisa's informed agreement and caregiving impact
- Actual hiring terms, pay, benefits, and job-search timeline
- Household budget and minimum income floor
- Household six-month cash flow and minimum savings floor.
- Lisa's genuine buy-in and childcare capacity.
- Job-fit evidence, target salary floor, and hiring traction.
- Lisa's explicit buy-in and agreed family limits
- Budget, savings floor, and job-search runway
- Whether software work suits him beyond a hobby
- Lisa's informed agreement and childcare limits; actual budget, cash floor and stopping rule.
- Software-as-work fit, hiring traction, likely pay, benefits and timeline.
- Peter Thiel просит проверить: Lisa's explicit agreement, childcare limits, household budget, cash floor and stopping rule.
- Peter Thiel просит проверить: A shipped domain project and actual market feedback, plus job-fit and compensation evidence.
- Warren Buffett просит проверить: Obtain household budget, cash floor, Lisa’s agreement, and a dated stopping rule.
- Warren Buffett просит проверить: Test paid-work fit and hiring response; establish salary floor and realistic timeline.
- Robert Reich просит проверить: Lisa's informed agreement and childcare limits, plus actual budget, income floor, and savings/job-search stopping rule.
- Robert Reich просит проверить: Evidence of paid-software fit and actual employer terms: pay, benefits, hiring conditions, and timeline.
- Nassim Nicholas Taleb просит проверить: Actual household budget, savings floor, childcare limits, and Lisa's agreement.
- Nassim Nicholas Taleb просит проверить: Evidence of paid-work fit, hiring traction, likely compensation, and timeline.
- Marcus Aurelius просит проверить: Lisa's informed agreement, childcare limits, actual household budget and savings floor.
- Marcus Aurelius просит проверить: Evidence of software-as-work fit, hiring response, likely pay and timeline.

## Источники и границы проверки

Загружено источников: 90; показано моделям: 34; chunks: 50.
Полный inventory, поисковые ранги, версии, голоса и происхождение цитат сохранены в trace.json.
Исходные даты досье не подтверждают актуальность сведений. Проверка substring не доказывает смысловую поддержку вывода.

- `e00115` · `corpus\doc_007.md` `/` [64:478]: "There's a quiet condescension in some corners of the software world toward\r\npeople coming from \"traditional\" engineering — as if mechanical or automotive\r\nwork is a lesser, slower discipline that the newcomer is lucky to escape. This\r\ngets the value transfer exactly backwards. Engineers from physical disciplines\r\narrive with a toolkit that many self-taught web developers spend years\r\nacquiring "
- `e00113` · `corpus\doc_006.md` `/` [3009:3506]: "The market is tougher than 2021 but far from closed, and the region offers a\r\nspecific edge: the overlap between traditional engineering/automotive domain\r\nknowledge and software demand. A candidate who can credibly say \"I understand\r\nboth how this physical product works *and* how to build the software around it\"\r\nis solving a hiring problem that pure-software juniors can't. That is a sharper\r\n"
- `e00024` · `user_kb.md` `/` [6259:6618]: "| Item | Amount |\r\n| --- | --- |\r\n| Mark base salary | $98,000 / yr |\r\n| Mark annual bonus | $5,000–$8,000 (variable) |\r\n| Lisa income (part-time) | ~$35,000 / yr |\r\n| Liquid savings | ~$42,000 |\r\n| 401k | Separate; treated as untouchable |\r\n| Mortgage | $1,750 / month |\r\n| Other significant debt | None |\r\n| Bootcamp option | $14,000 tuition, 6 months |\r\n\r\n"
- `e00025` · `user_kb.md` `/` [6618:7151]: "The headline tension: the bootcamp's $14k tuition is affordable on paper, but\r\nthe family's margin is thin. If Mark left his job to attend full-time, the\r\nhousehold would drop to Lisa's ~$35k while burning savings on both living costs\r\nand tuition. Six months of that could consume most of the $42k cushion. If he\r\nkeeps working and studies part-time, the money is safe but the timeline\r\nstretches "
- `e00016` · `user_kb.md` `/` [3784:4893]: "- **Financial runway.** The family has roughly $42,000 in liquid savings (the\r\n  401k is separate and he considers it untouchable). The mortgage is\r\n  $1,750/month. A six-month, $14,000 bootcamp would consume both tuition and a\r\n  meaningful chunk of runway if he stopped working.\r\n- **Time.** Mark has a demanding full-time job and a three-year-old. His study\r\n  time is genuinely scarce — evenings "
- `e00253` · `notes.json` `/29` [0:387]: "{\"content\":\"Tried to count my real study hours this week: maybe 6, scattered, mostly after 10pm. At this rate self-study could take another two years to get job-ready, if I don't burn out first. That's the honest case against 'just keep studying on the side.' The slow path isn't risk-free either — it's just a different risk.\",\"date\":\"2024-06-12\",\"note_id\":\"n_030\",\"title\":\"Time audit\"}"
- `e00013` · `user_kb.md` `/` [3024:3414]: "- To do work that engages him intellectually the way coding currently does.\r\n- To increase his earning potential. He has friends in tech earning 1.5x to\r\n  2x his salary, and he is acutely aware of the gap.\r\n- To feel some control over his career trajectory rather than waiting for the\r\n  next reorg to decide his fate.\r\n- Not to blow up his family's financial stability in the process.\r\n\r\n"
- `e00245` · `notes.json` `/21` [0:372]: "{\"content\":\"Honest 1am fear: what if I love coding as a hobby and hate it as a job? Hobbies don't have standups and Jira and a manager breathing down your neck about a sprint. Maybe the thing I actually love is that nobody's paying me to do it. How would I even test that before betting the family on it?\",\"date\":\"2024-05-01\",\"note_id\":\"n_022\",\"title\":\"What if I hate it\"}"
- `e00249` · `notes.json` `/25` [0:381]: "{\"content\":\"If I'm going to convince anyone to hire me, the expense tracker isn't enough. Need one real, polished, deployed project that solves an actual problem. Maybe something using my automotive domain knowledge — a parts/inventory tool? Lean into the thing I already know instead of pretending I'm a fresh grad.\",\"date\":\"2024-05-16\",\"note_id\":\"n_026\",\"title\":\"Portfolio idea\"}"

Раундов: 1; model attempts: 28; время: 69.02 с.
