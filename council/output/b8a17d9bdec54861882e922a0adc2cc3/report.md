# Отчёт совета пяти персон

Статус: **failed**

RuntimeError: protocol/source/model failure

Режим: `model`. Режим выбранного LLM-провайдера. Формальное согласие не доказывает качество решения.

Вопрос: I'm thinking about switching careers from mechanical engineering to software development. Help me think through this decision.

Человек принимает итоговое решение после отчёта. Его выбор не меняет статус согласия персон.

Условный тестовый режим AI Tunnel. Превышения запрошенного лимита допускаются только до отдельного жёсткого потолка; этот профиль не предназначен для production.
Запрошено: 2000 токенов; потолок приёма: 8000; полученных ответов с превышением: 5.

Провайдер: `aitunnel`; модель: `gpt-6-luna-pro`; учёт контекста: `server_enforced`.

Reasoning effort: `none`. Эта настройка влияет на расход и качество модели; none используется для проверки процесса.

Предварительный count OpenAI ограничивает бюджет приложения, не подтверждает окно любой модели. AI Tunnel проверяет переполнение на сервере без точного предварительного count; сжатие отключено.

Лимит попыток относится к локальным запросам. Внутренние повторы провайдера и расходы после отмены неизвестны. Usage полученных ответов, включая отклонённые, сохранён в trace; отсутствующие данные не означают нулевой расход.

## Рекомендация и план

My position: do not quit for bootcamp now; first run a bounded, employed trial and decide from evidence. Strongest counterargument: scarce, scattered study time may extend the transition and increase burnout risk, so a structured bootcamp could be faster. That speed does not establish safe finances or job fit; revisit the choice only after Lisa and Mark agree on the budget, reserve, time limits, fallback, and target.

Шаги:

1. Before spending substantially or changing work hours, review household cash flow with Lisa, agree on a minimum savings floor and salary floor, and define a stopping rule and 12-month success target.
2. Agree on a manageable trial period and schedule while employed. Include a low-cost way to experience software work as work, not only hobby coding; assess enjoyment and family-time impact.
3. Build and deploy one polished project addressing a real automotive or mechanical problem, then seek feedback and conversations with relevant employers or practitioners.
4. At the agreed review date, compare trial evidence, household effects, and actual hiring/pay information with the pre-agreed guardrails. Continue, change approach, or stop; do not presume an offer, salary gain, or bootcamp outcome.

Альтернативы:

- Quit for full-time bootcamp now; faster structure, but exposes household savings and income.
- Keep working and run a bounded software-as-work trial before deciding whether to pursue a bootcamp or continue self-study.

## Риски и условия решения

- Monthly spending, minimum savings reserve, Lisa’s informed agreement, salary floor, and 12-month success target are unknown; the trial must not be treated as proof that a later switch is financially safe.
- The trial’s duration and workload are proposed, not established as feasible; adjust them with Lisa and protect family time.

Проверенная версия 1, digest `61f4207357610040e703273b152f90a04a72f3f40ecb437460bcc84d49b2bb4a`. Полный неизменный JSON решения сохранён в trace.json.

## Пять позиций и текущие оценки

### Peter Thiel

Build a domain-specific software project while employed; test the work and agree guardrails before any bootcamp leap.

Аргументы этого взгляда:

- Your edge isn’t credentials: it’s pairing mechanical/automotive insight with shipped software solving a real domain problem.
- Don’t quit for bootcamp yet: the $14k cost plus lost income risks the family cushion, and Lisa’s real buy-in is unresolved.

Критерии:

- Commit only after testing software-as-work, Lisa’s genuine buy-in, household floor/runway and a stopping rule; then choose a path that ships domain-specific proof.
Контраргумент: Self-study risks dragging on: about six scattered hours weekly could mean two years to job-ready; a structured bootcamp may accelerate proof.

Текущий голос не получен.

### Warren Buffett

Circle of competence first, margin of safety always: test software without quitting; reserve a leap for proven fit and guarded finances.

Аргументы этого взгляда:

- Keep the engineering paycheck; do not fund a full-time bootcamp from the family cushion.
- Test software while employed: ship a domain-informed project and build local connections.

Критерии:

- Proceed only after Lisa's genuine buy-in, a household budget and savings floor, and evidence you want software work—not merely escape boredom; otherwise defer the leap.
Контраргумент: Six evening hours weekly may stretch readiness toward two years; delay has costs, while engineering-software overlap could open a better path.

Текущий голос не получен.

### Robert Reich

Explore software without quitting yet; test the work and hiring market while protecting family income.

Аргументы этого взгляда:

- A switch fits your goals, but quitting for bootcamp risks savings and shifts childcare and income strain onto Lisa.
- Software’s upside is not an immediate pay rise; local first-role estimates can fall below your current high-$90k salary.

Критерии:

- Choose only after you confirm you want software, model household cash flow and a salary floor, secure Lisa’s genuine buy-in, and set a savings/time stopping rule; verify actual hiring terms and benefits.
Контраргумент: Staying put is not risk-free: layoffs have happened, and scarce study hours may make self-study slow and exhausting.

Текущий голос не получен.

### Nassim Nicholas Taleb

Don't quit yet. Run a bounded software trial while employed; preserve the option to switch, not the fantasy of a guaranteed payoff.

Аргументы этого взгляда:

- Full-time bootcamp risks the family cushion: $14k tuition plus lost income could consume much of $42k savings.
- But hobby-to-job fit is untested; roughly six scattered weekly study hours make the slow path a real burnout risk.

Критерии:

- Favor reversible exposure: keep income, test day-to-day software work and ship a domain-linked project; only escalate with Lisa's buy-in, a household-checked loss limit and fallback.
Контраргумент: Self-study may stretch for years and drain morale; a switch could unlock more engaging work and earnings, but neither timing nor salary is assured.

Текущий голос не получен.

### Marcus Aurelius

Choose a bounded, working-while-learning trial; decide on evidence, not status anxiety or fear.

Аргументы этого взгляда:

- Keep working while testing software through a shipped project and real conversations; avoid quitting for bootcamp now.
- But scattered study may take years, and hobby coding may not suit paid work; test that directly rather than drift.

Критерии:

- Switch only after Lisa's genuine buy-in, a tested career fit, a household-safe runway and stopping rule, and a clear 12-month success target.
Контраргумент: Six hours of scattered study may prolong uncertainty; a structured bootcamp could build skills faster, but quitting risks the family's cushion.

Текущий голос не получен.

## Возражения и противоречия

Зафиксированных возражений/противоречий нет. Это не доказательство их отсутствия в досье.

## Недостающие данные

- 12-month success definition
- Household minimum salary/runway
- Lisa’s genuine buy-in and stopping rule
- Full household spending and affordable savings floor.
- Lisa's buy-in; job-search timeline and acceptable salary floor.
- Evidence of fit with software as paid work.
- Lisa’s informed agreement
- Household budget and minimum salary
- Employer offers, benefits, hiring terms
- Household budget, essential expenses and minimum savings floor.
- Lisa's genuine buy-in and acceptable family time cost.
- Software-job trial results and defined success/pay floor.
- Monthly household spending and minimum reserve.
- Lisa's genuine agreement and preferred guardrails.
- Job-market fit, salary floor, and a concrete 12-month target.
- Actual monthly household spending and agreed minimum savings floor.
- Lisa’s informed preference, family-time limits, and acceptable stopping rule.
- A salary floor, benefits needs, and specific 12-month success target.

## Источники и границы проверки

Загружено источников: 90; показано моделям: 36; chunks: 52.
Полный inventory, поисковые ранги, версии, голоса и происхождение цитат сохранены в trace.json.
Исходные даты досье не подтверждают актуальность сведений. Проверка substring не доказывает смысловую поддержку вывода.

- `e00113` · `corpus\doc_006.md` `/` [3009:3506]: "The market is tougher than 2021 but far from closed, and the region offers a\r\nspecific edge: the overlap between traditional engineering/automotive domain\r\nknowledge and software demand. A candidate who can credibly say \"I understand\r\nboth how this physical product works *and* how to build the software around it\"\r\nis solving a hiring problem that pure-software juniors can't. That is a sharper\r\n"
- `e00249` · `notes.json` `/25` [0:381]: "{\"content\":\"If I'm going to convince anyone to hire me, the expense tracker isn't enough. Need one real, polished, deployed project that solves an actual problem. Maybe something using my automotive domain knowledge — a parts/inventory tool? Lean into the thing I already know instead of pretending I'm a fresh grad.\",\"date\":\"2024-05-16\",\"note_id\":\"n_026\",\"title\":\"Portfolio idea\"}"
- `e00025` · `user_kb.md` `/` [6618:7151]: "The headline tension: the bootcamp's $14k tuition is affordable on paper, but\r\nthe family's margin is thin. If Mark left his job to attend full-time, the\r\nhousehold would drop to Lisa's ~$35k while burning savings on both living costs\r\nand tuition. Six months of that could consume most of the $42k cushion. If he\r\nkeeps working and studies part-time, the money is safe but the timeline\r\nstretches "
- `e00238` · `notes.json` `/14` [0:395]: "{\"content\":\"Brought up the bootcamp idea seriously for the first time. Lisa said she'd support whatever I decide. But the way she said it was tight — that flat voice she uses when she's worried but doesn't want a fight. I think she's scared about the money and I don't blame her. I need to bring her a real plan, not a feeling.\",\"date\":\"2024-04-02\",\"note_id\":\"n_015\",\"title\":\"Lisa conversation\"}"
- `e00024` · `user_kb.md` `/` [6259:6618]: "| Item | Amount |\r\n| --- | --- |\r\n| Mark base salary | $98,000 / yr |\r\n| Mark annual bonus | $5,000–$8,000 (variable) |\r\n| Lisa income (part-time) | ~$35,000 / yr |\r\n| Liquid savings | ~$42,000 |\r\n| 401k | Separate; treated as untouchable |\r\n| Mortgage | $1,750 / month |\r\n| Other significant debt | None |\r\n| Bootcamp option | $14,000 tuition, 6 months |\r\n\r\n"
- `e00253` · `notes.json` `/29` [0:387]: "{\"content\":\"Tried to count my real study hours this week: maybe 6, scattered, mostly after 10pm. At this rate self-study could take another two years to get job-ready, if I don't burn out first. That's the honest case against 'just keep studying on the side.' The slow path isn't risk-free either — it's just a different risk.\",\"date\":\"2024-06-12\",\"note_id\":\"n_030\",\"title\":\"Time audit\"}"
- `e00013` · `user_kb.md` `/` [3024:3414]: "- To do work that engages him intellectually the way coding currently does.\r\n- To increase his earning potential. He has friends in tech earning 1.5x to\r\n  2x his salary, and he is acutely aware of the gap.\r\n- To feel some control over his career trajectory rather than waiting for the\r\n  next reorg to decide his fate.\r\n- Not to blow up his family's financial stability in the process.\r\n\r\n"
- `e00016` · `user_kb.md` `/` [3784:4893]: "- **Financial runway.** The family has roughly $42,000 in liquid savings (the\r\n  401k is separate and he considers it untouchable). The mortgage is\r\n  $1,750/month. A six-month, $14,000 bootcamp would consume both tuition and a\r\n  meaningful chunk of runway if he stopped working.\r\n- **Time.** Mark has a demanding full-time job and a three-year-old. His study\r\n  time is genuinely scarce — evenings "
- `e00016` · `user_kb.md` `/` [3784:4893]: "most of the childcare\r\n  load already. Any plan that further reduces Mark's availability at home has a\r\n  real cost that lands on her.\r\n- **Risk tolerance.** Mark is constitutionally cautious. A plan that is\r\n  financially sound but psychologically reckless (for him) is not actually a\r\n  fit, and vice versa.\r\n\r\n"
- `e00109` · `corpus\doc_006.md` `/` [1898:2468]: "Midwest software salaries run below coastal numbers but so does the cost of\r\nliving, and the ratio is favorable. A first software role for a career changer\r\nin metro Detroit might land somewhere in the $70k-$95k range depending on the\r\nemployer and the candidate's portfolio; mid-level roles climb into the\r\nsix-figure range; senior roles comfortably exceed it. For someone currently\r\nearning in the "
- `e00187` · `corpus\doc_012.md` `/` [907:1621]: "For many career changers, the first software offer is at or slightly below their\r\nprevious salary. If you were earning, say, in the high $90ks in another\r\nengineering field, a first junior-dev offer in the $70k-$90k range is common and\r\nnot an insult — it reflects that you're junior *in this field*, even if senior\r\nin life. The mistake is to either (a) be so wounded by the number that you\r\nreject "
- `e00297` · `tasker:get_task_details` `/t_010` [0:299]: "{\"description\":\"Find low-cost ways to experience software work as work, not hobby, before betting the family on it.\",\"due_date\":\"2024-08-01\",\"notes\":\"The 1am fear: loving the hobby but hating the job.\",\"status\":\"not_started\",\"task_id\":\"t_010\",\"title\":\"Pressure-test the 'I'd hate it as a job' fear\"}"
- `e00245` · `notes.json` `/21` [0:372]: "{\"content\":\"Honest 1am fear: what if I love coding as a hobby and hate it as a job? Hobbies don't have standups and Jira and a manager breathing down your neck about a sprint. Maybe the thing I actually love is that nobody's paying me to do it. How would I even test that before betting the family on it?\",\"date\":\"2024-05-01\",\"note_id\":\"n_022\",\"title\":\"What if I hate it\"}"

Раундов: 1; model attempts: 32; время: 66.70 с.
