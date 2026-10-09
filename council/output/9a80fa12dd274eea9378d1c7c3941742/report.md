# Отчёт совета пяти персон

Статус: **failed**

RuntimeError: protocol/source/model failure

Режим: `model`. Режим выбранного LLM-провайдера. Формальное согласие не доказывает качество решения.

Вопрос: I'm thinking about switching careers from mechanical engineering to software development. Help me think through this decision.

Человек принимает итоговое решение после отчёта. Его выбор не меняет статус согласия персон.

Условный тестовый режим AI Tunnel. Превышения запрошенного лимита допускаются только до отдельного жёсткого потолка; этот профиль не предназначен для production.
Запрошено: 2000 токенов; потолок приёма: 8000; полученных ответов с превышением: 0.

Провайдер: `aitunnel`; модель: `gpt-6-luna-pro`; учёт контекста: `server_enforced`.

Reasoning effort: `none`. Эта настройка влияет на расход и качество модели; none используется для проверки процесса.

Предварительный count OpenAI ограничивает бюджет приложения, не подтверждает окно любой модели. AI Tunnel проверяет переполнение на сервере без точного предварительного count; сжатие отключено.

Лимит попыток относится к локальным запросам. Внутренние повторы провайдера и расходы после отмены неизвестны. Usage полученных ответов, включая отклонённые, сохранён в trace; отсутствующие данные не означают нулевой расход.

Согласованного проекта нет; анализ не завершён.

## Пять позиций и текущие оценки

### Peter Thiel

Test the software path while employed; build a domain-specific project, then decide from evidence—not credential anxiety.

Аргументы этого взгляда:

- What edge does a generic junior lack? Pair mechanical domain knowledge with shipped software—not credentials.
- Quit-and-bootcamp concentrates downside: $14k tuition, one income, and thin savings.

Критерии:

- Choose software only after testing job-fit and earning a real portfolio/network signal; preserve household runway, Lisa's buy-in, and a pre-agreed stop rule.
Контраргумент: At six scattered study hours weekly, self-study may drag on; delay also risks burnout and lost opportunity.

Текущий голос не получен.

### Warren Buffett

Stay employed; test software with a domain-based project before risking the emergency cushion on a bootcamp.

Аргументы этого взгляда:

- A full-time bootcamp risks the family cushion: tuition plus six months without Mark's salary.
- Self-study is slow at six scattered hours weekly; engineering-domain software work may offer a differentiated path.

Критерии:

- Choose a bounded experiment only after cash-flow math, Lisa's genuine buy-in, and a clear stopping rule; first test whether software is the goal and job-fit.
Контраргумент: Staying safe can become a costly delay: limited study time may stretch self-study toward two years, while the first software role may pay less.

Текущий голос не получен.

### Robert Reich

Run a bounded, job-preserving transition experiment before committing savings or income.

Аргументы этого взгляда:

- Keep your job while testing software with a domain-based project; don’t quit for bootcamp yet.
- But part-time study is slow, and a first software offer may pay less; staying put is not risk-free.

Критерии:

- Before quitting, confirm Lisa’s genuine buy-in, household cash flow and a stopping rule; test job fit, and verify actual offers, pay and benefits against your family’s floor.
Контраргумент: Waiting risks burnout and prolongs a path with scarce study time; bootcamp may accelerate progress, but its employment payoff is unknown.

Текущий голос не получен.

### Nassim Nicholas Taleb

Don't quit now. Test software while employed; preserve the option to switch, not the emergency cushion.

Аргументы этого взгляда:

- A full-time bootcamp is a fragile bet: tuition plus lost income could consume much of savings.
- Self-study preserves income, but scarce hours may stretch the path; liking coding as a hobby proves little about job fit.

Критерии:

- Choose a reversible trial: keep income, validate job-fit and a domain-linked portfolio; only consider bootcamp after verified cash-flow, Lisa's genuine buy-in, and explicit savings/time stopping rules.
Контраргумент: At roughly six scattered study hours weekly, the safe path may become a two-year stall; bootcamp could accelerate progress, but outcomes and fit are uncertain.

Текущий голос не получен.

### Marcus Aurelius

Do not leap yet: run a family-approved, bounded test of software while protecting income and daily duties.

Аргументы этого взгляда:

- There is a real pull toward engaging work, better earnings and career agency—but preserve family stability.
- Quitting for a $14k, six-month bootcamp risks the savings cushion; scattered self-study may be slow and draining.

Критерии:

- Choose a bounded next step only after Lisa and I agree on a budget, runway floor and stopping rule; test job-fit and ship a domain-informed project while keeping work and family practice sustainable.
Контраргумент: The slow path is not harmless: six scattered study hours weekly may prolong uncertainty and exhaustion.

Текущий голос не получен.

## Возражения и противоречия

Зафиксированных возражений/противоречий нет. Это не доказательство их отсутствия в досье.

## Недостающие данные

- Lisa's genuine buy-in
- Household budget and minimum acceptable salary
- Job-fit test and portfolio/network results
- Six-month household cash-flow
- 12-month success measure and job-fit test
- Six-month cash-flow details and household minimum income.
- Lisa’s considered agreement and acceptable workload.
- Actual hiring offers, benefits and conditions.
- Verified 6-month household cash flow
- Whether software is a pull, not escape
- Household expenses and agreed savings floor
- Whether software itself, not escape, is the goal
- Job-fit evidence and tolerable first-role salary

## Источники и границы проверки

Загружено источников: 90; показано моделям: 34; chunks: 50.
Полный inventory, поисковые ранги, версии, голоса и происхождение цитат сохранены в trace.json.
Исходные даты досье не подтверждают актуальность сведений. Проверка substring не доказывает смысловую поддержку вывода.

- `e00113` · `corpus\doc_006.md` `/` [3009:3506]: "The market is tougher than 2021 but far from closed, and the region offers a\r\nspecific edge: the overlap between traditional engineering/automotive domain\r\nknowledge and software demand. A candidate who can credibly say \"I understand\r\nboth how this physical product works *and* how to build the software around it\"\r\nis solving a hiring problem that pure-software juniors can't. That is a sharper\r\n"
- `e00249` · `notes.json` `/25` [0:381]: "{\"content\":\"If I'm going to convince anyone to hire me, the expense tracker isn't enough. Need one real, polished, deployed project that solves an actual problem. Maybe something using my automotive domain knowledge — a parts/inventory tool? Lean into the thing I already know instead of pretending I'm a fresh grad.\",\"date\":\"2024-05-16\",\"note_id\":\"n_026\",\"title\":\"Portfolio idea\"}"
- `e00016` · `user_kb.md` `/` [3784:4893]: "- **Financial runway.** The family has roughly $42,000 in liquid savings (the\r\n  401k is separate and he considers it untouchable). The mortgage is\r\n  $1,750/month. A six-month, $14,000 bootcamp would consume both tuition and a\r\n  meaningful chunk of runway if he stopped working.\r\n- **Time.** Mark has a demanding full-time job and a three-year-old. His study\r\n  time is genuinely scarce — evenings "
- `e00230` · `notes.json` `/6` [0:429]: "{\"content\":\"Codesmith Detroit is $14k, 6 months full-time. We have ~$42k saved. If I quit, household drops to Lisa's ~$35k. Six months of mortgage ($1,750) + living + tuition... math is tight but possible. Maybe. The ISA option means no tuition up front but you pay a chunk of salary later. Need to actually run the numbers instead of doing this in my head at "
- `e00025` · `user_kb.md` `/` [6618:7151]: "The headline tension: the bootcamp's $14k tuition is affordable on paper, but\r\nthe family's margin is thin. If Mark left his job to attend full-time, the\r\nhousehold would drop to Lisa's ~$35k while burning savings on both living costs\r\nand tuition. Six months of that could consume most of the $42k cushion. If he\r\nkeeps working and studies part-time, the money is safe but the timeline\r\nstretches "
- `e00253` · `notes.json` `/29` [0:387]: "{\"content\":\"Tried to count my real study hours this week: maybe 6, scattered, mostly after 10pm. At this rate self-study could take another two years to get job-ready, if I don't burn out first. That's the honest case against 'just keep studying on the side.' The slow path isn't risk-free either — it's just a different risk.\",\"date\":\"2024-06-12\",\"note_id\":\"n_030\",\"title\":\"Time audit\"}"
- `e00013` · `user_kb.md` `/` [3024:3414]: "- To do work that engages him intellectually the way coding currently does.\r\n- To increase his earning potential. He has friends in tech earning 1.5x to\r\n  2x his salary, and he is acutely aware of the gap.\r\n- To feel some control over his career trajectory rather than waiting for the\r\n  next reorg to decide his fate.\r\n- Not to blow up his family's financial stability in the process.\r\n\r\n"
- `e00109` · `corpus\doc_006.md` `/` [1898:2468]: "Midwest software salaries run below coastal numbers but so does the cost of\r\nliving, and the ratio is favorable. A first software role for a career changer\r\nin metro Detroit might land somewhere in the $70k-$95k range depending on the\r\nemployer and the candidate's portfolio; mid-level roles climb into the\r\nsix-figure range; senior roles comfortably exceed it. For someone currently\r\nearning in the "
- `e00024` · `user_kb.md` `/` [6259:6618]: "| Item | Amount |\r\n| --- | --- |\r\n| Mark base salary | $98,000 / yr |\r\n| Mark annual bonus | $5,000–$8,000 (variable) |\r\n| Lisa income (part-time) | ~$35,000 / yr |\r\n| Liquid savings | ~$42,000 |\r\n| 401k | Separate; treated as untouchable |\r\n| Mortgage | $1,750 / month |\r\n| Other significant debt | None |\r\n| Bootcamp option | $14,000 tuition, 6 months |\r\n\r\n"
- `e00245` · `notes.json` `/21` [0:372]: "{\"content\":\"Honest 1am fear: what if I love coding as a hobby and hate it as a job? Hobbies don't have standups and Jira and a manager breathing down your neck about a sprint. Maybe the thing I actually love is that nobody's paying me to do it. How would I even test that before betting the family on it?\",\"date\":\"2024-05-01\",\"note_id\":\"n_022\",\"title\":\"What if I hate it\"}"

Раундов: 0; model attempts: 22; время: 56.38 с.
