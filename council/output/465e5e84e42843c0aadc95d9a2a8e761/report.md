# Отчёт совета пяти персон

Статус: **incomplete**

context_overflow: pinned closure

Режим: `model`. Режим выбранного LLM-провайдера. Формальное согласие не доказывает качество решения.

Вопрос: I'm thinking about switching careers from mechanical engineering to software development. Help me think through this decision.

Человек принимает итоговое решение после отчёта. Его выбор не меняет статус согласия персон.

Условный тестовый режим AI Tunnel. Превышения запрошенного лимита допускаются только до отдельного жёсткого потолка; этот профиль не предназначен для production.
Запрошено: 2000 токенов; потолок приёма: 8000; полученных ответов с превышением: 1.

Провайдер: `aitunnel`; модель: `gpt-6-luna-pro`; учёт контекста: `server_enforced`.

Reasoning effort: `none`. Эта настройка влияет на расход и качество модели; none используется для проверки процесса.

Предварительный count OpenAI ограничивает бюджет приложения, не подтверждает окно любой модели. AI Tunnel проверяет переполнение на сервере без точного предварительного count; сжатие отключено.

Лимит попыток относится к локальным запросам. Внутренние повторы провайдера и расходы после отмены неизвестны. Usage полученных ответов, включая отклонённые, сохранён в trace; отсутствующие данные не означают нулевой расход.

## Рекомендация и план

My position: do not quit or commit to the $14,000 bootcamp yet. While employed, test software as work and build a useful, deployed automotive-domain project; seek local employer feedback. With Lisa, calculate actual household cash flow, agree on a savings floor and fallback, and set a review date and success measures. Then compare employed training options against verified hiring requirements and compensation. Strongest counterargument: scarce evening study may prolong the transition or cause burnout, and structured training could accelerate it; that possibility warrants a review, not an unverified leap.

Шаги:

1. Clarify whether the goal is software work itself or escape from current dissatisfaction; define a practical success measure and review date.
2. With Lisa, map expenses, available study time, childcare impact, savings floor, and a fallback before choosing a schedule or spending.
3. Build and deploy one focused automotive/mechanical software project; use job-like tasks and conversations with local employers to test fit and demand.
4. At the agreed review, compare continued employment, part-time training, and bootcamp using verified costs, requirements, compensation, and household guardrails; do not infer a job outcome.

Альтернативы:

- Keep working and run a time-bounded software-fit and market test before deciding.
- Compare part-time study, a bootcamp while employed, and a later transition after household finances and family agreement are clear.

## Риски и условия решения

- A part-time trial may be difficult to sustain; actual household expenses, available hours, Lisa’s view, and an agreed savings floor are unknown. Confirm these before setting a timeline or making a financial commitment.
- Project interest and local employer feedback do not establish job placement, timing, or compensation. Verify hiring requirements and household affordability before changing employment.

Проверенная версия 1, digest `a1ea543f08b731b65de426362ed3a21a02ebf4debca715a3a129e217b380ce2e`. Полный неизменный JSON решения сохранён в trace.json.

## Пять позиций и текущие оценки

### Peter Thiel

Don’t decide by credential anxiety or bootcamp marketing. Preserve the job while testing the differentiated thesis: ship the domain project, talk to local employers, and test work-like software tasks. If the motivation holds, Lisa agrees, and the verified runway supports a bounded transition, compare bootcamp against self-study on realistic timelines. Otherwise stay employed and revisit with evidence.

Аргументы этого взгляда:

- The unfair advantage isn’t a credential: it’s knowing the physical engineering problem well enough to build software for it. Test that edge with a deployed automotive-domain project; don’t compete as a generic junior.
- A full-time bootcamp is a concentrated bet, but quitting risks the family’s thin runway. First get real cash-flow numbers and Lisa’s genuine buy-in; agree a savings floor and stopping rule before committing.
- Before choosing a path, answer the harder question: are you moving toward software or away from boredom—and have you tested whether you’d like it as paid work?

Критерии:

- Clarify what success means and test whether the motivation is toward software, not merely away from mechanical engineering.
- No full-time exit without verified cash-flow, Lisa’s genuine agreement, and explicit downside guardrails.
- Build and ship a polished project using automotive/mechanical domain knowledge; assess market response, not credentials alone.
Контраргумент: Part-time study is not free of risk: scarce evenings may stretch preparation for years and burn you out. A bootcamp could accelerate learning and focus—but its timeline and placement are uncertain, while leaving work could consume much of the savings cushion. That case needs verified numbers and family agreement, not optimism.

Текущий голос не получен.

### Warren Buffett

Stay employed for now. Before spending $14,000 or surrendering income, run the real six-month budget, agree with Lisa on a savings floor and fallback, and test job-like coding through a deployed engineering-related project and conversations with local employers. Set a review date and success measures; revisit bootcamp only if the evidence and finances support it. Staying put remains a valid option, not a failure.

Аргументы этого взгляда:

- Lead with the downside: don’t quit for a bootcamp before the household cash-flow is known and Lisa genuinely agrees.
- There is a credible edge in pairing engineering knowledge with software. Build and deploy one useful automotive project while employed, then test it with local employers.
- The strongest counterargument: evenings-only study is already slow, and hobby coding may not resemble software work. Treat the employed trial as an experiment, not proof.
- Assumption: an employed, time-bounded trial is feasible; confirm with Lisa and actual schedules.

Критерии:

- Protect household runway; do not recommend leaving employment until actual cash-flow and a shared stopping rule are agreed.
- Test software as work and clarify whether the pull is toward software or away from current dissatisfaction.
- Favor a practical, domain-specific portfolio and employer conversations over competing as a generic junior.
Контраргумент: The slow path is not free: limited evening hours may prolong uncertainty and create burnout, while a focused bootcamp could accelerate learning. But its benefit is uncertain, and the current record does not establish that the family can absorb the downside or that Mark has tested software as a job.

Текущий голос не получен.

### Robert Reich

Do not quit yet. First run the household cash-flow numbers with Lisa, agree on a savings floor and fallback, and test job fit and employer demand through a shipped automotive-domain project and targeted conversations. Then compare bootcamp, part-time study, and staying in engineering against real hiring requirements and compensation—including benefits and any pay cut. The switch may be worth pursuing, but neither higher pay nor a quick placement is established.

Аргументы этого взгляда:

- A switch fits your goals, but not as a blind leap: you want engaging work and higher earning potential without destabilizing your family, and a first Detroit software role may pay less than your current high-$90k salary.
- The bootcamp’s price is only part of the cost: quitting shifts income and runway risk onto your household, while extra study time also lands on Lisa. Get her genuine buy-in and agree on a cash floor and stopping rule first.
- My recommendation: keep your job for now; test whether you want software work through a deployed domain-informed project, conversations with local employers, and a realistic budget before choosing bootcamp or a longer study path.

Критерии:

- Determine whether Mark is moving toward software work or away from dissatisfaction, and define what success means.
- Do not recommend quitting or committing to bootcamp until cash flow, Lisa’s genuine buy-in, and a savings stopping rule are addressed.
- Assess actual hiring conditions, first-role pay, benefits, and fallback options; do not assume higher earnings.
Контраргумент: The cautious path is not risk-free: study time is scarce and scattered, and prolonged self-study may stretch for years or burn you out. Your engineering background and automotive knowledge may help differentiate you, while a bootcamp could accelerate skills and connections. But that case supports a bounded experiment, not betting the family’s emergency cushion without verified finances, Lisa’s buy-in, and realistic employer evidence.

Текущий голос не получен.

### Nassim Nicholas Taleb

Do not resign or spend $14,000 yet. Keep the job, finish a deployed domain-relevant project, test day-to-day software work and employer interest, and build a household budget with Lisa. Set a savings floor and a dated review point in advance; consider paid training only if the evidence justifies it and the downside stays bounded. A first software offer could be below current pay, so establish the household’s minimum acceptable number before interviews.

Аргументы этого взгляда:

- The goal is not “software at any cost”: Mark wants more engaging work and earning potential without risking family stability. Run a bounded test before quitting.
- The bootcamp’s $14,000 tuition plus lost income could consume much of the savings; current study time is scarce. Don’t pretend either path has a guaranteed timeline.
- Build and deploy a real project using mechanical/automotive knowledge, talk to local employers, and agree with Lisa on a savings floor and deadline before committing further.
- Assuming Mark can keep working while testing, this is more reversible than quitting for full-time training.

Критерии:

- Does the next step cap financial and family downside rather than relying on an optimistic placement timeline?
- Does it test whether software work itself fits and whether employers value the combined domain/software profile?
Контраргумент: The slow route is not safe by default: study time is scarce and could mean a long, draining transition. Mark has described losing interest in current engineering work, and a targeted program might accelerate a credible switch. But acceleration is not proof of placement; buy it only after fit, finances, and outcomes are checked.

Текущий голос не получен.

### Marcus Aurelius

Choose a reversible experiment before an irreversible leap. Keep the job healthy, ship a focused project, and get real financial numbers and Lisa's buy-in. Then compare the evidence with a pre-agreed savings floor and fallback. Ambition is not proof; neither is fear. What can you do consistently without shifting an unfair cost onto your family?

Аргументы этого взгляда:

- Do not resign for a bootcamp yet. First test the path while employed and make a shared, written budget and fallback with Lisa.
- Build and deploy one automotive-related software project; speak with local practitioners and test whether you want software work, not merely an escape from boredom.
- Assumption: a sustainable part-time trial is feasible alongside current duties. Agree on modest weekly hours, a review date, and a savings floor before committing.

Критерии:

- Avoid risking household stability without current cash-flow numbers, a savings floor, and Lisa's genuine agreement.
- Test interest and employability through shipped work and conversations, not fear or salary comparisons alone.
Контраргумент: Part-time study is already slow and tiring, and waiting may prolong dissatisfaction; a structured bootcamp could accelerate learning and focus. But its cost and uncertain placement make quitting imprudent before cash flow, family agreement, and the fit test are settled.

Текущий голос не получен.

## Возражения и противоречия

Зафиксированных возражений/противоречий нет. Это не доказательство их отсутствия в досье.

## Недостающие данные

- Actual household expenses, six-month cash-flow, and minimum acceptable savings floor.
- Lisa’s considered view and a concrete plan for childcare and study time.
- Evidence from testing software work as a job and hiring-market feedback on a shipped project.
- Monthly household spending and minimum emergency reserve.
- Lisa’s genuine preference and feasible family-time limits.
- A defined success measure and stopping rule for the trial.
- Whether the primary motive is software itself, dissatisfaction, or burnout.
- Household spending and essential-expense runway; minimum acceptable savings and decision deadline.
- Lisa’s specific support, childcare impact, and acceptable transition burden.
- Current local employer openings, hiring criteria, benefits, and credible compensation offers.
- Whether a software job’s day-to-day work is appealing, and a concrete 12-month success measure.
- Household spending, minimum emergency reserve, and acceptable salary floor.
- Bootcamp outcomes and terms; local employer demand; realistic search duration.
- Lisa’s specific concerns and mutually agreed guardrails.
- Whether dissatisfaction is burnout, lack of interest in the current role, or positive attraction to software.
- Current monthly household spending and the actual runway under each option.
- Lisa's considered view and workable division of time and childcare.
- A defined success measure and deadline for deciding whether the trial supports a switch.
- Evidence that the software work and likely entry-level compensation fit the household.
- Household spending and verified runway; Lisa’s considered view and feasible childcare/time arrangement.
- A defined success measure, review date, savings floor, fallback, and minimum acceptable compensation.
- Current local openings, employer requirements, benefits, training outcomes, and credible placement timelines.

## Источники и границы проверки

Загружено источников: 90; показано моделям: 34; chunks: 50.
Полный inventory, поисковые ранги, версии, голоса и происхождение цитат сохранены в trace.json.
Исходные даты досье не подтверждают актуальность сведений. Проверка substring не доказывает смысловую поддержку вывода.

- `e00113` · `corpus\doc_006.md` `/` [3009:3506]: "The market is tougher than 2021 but far from closed, and the region offers a\r\nspecific edge: the overlap between traditional engineering/automotive domain\r\nknowledge and software demand. A candidate who can credibly say \"I understand\r\nboth how this physical product works *and* how to build the software around it\"\r\nis solving a hiring problem that pure-software juniors can't. That is a sharper\r\n"
- `e00249` · `notes.json` `/25` [0:381]: "{\"content\":\"If I'm going to convince anyone to hire me, the expense tracker isn't enough. Need one real, polished, deployed project that solves an actual problem. Maybe something using my automotive domain knowledge — a parts/inventory tool? Lean into the thing I already know instead of pretending I'm a fresh grad.\",\"date\":\"2024-05-16\",\"note_id\":\"n_026\",\"title\":\"Portfolio idea\"}"
- `e00025` · `user_kb.md` `/` [6618:7151]: "The headline tension: the bootcamp's $14k tuition is affordable on paper, but\r\nthe family's margin is thin. If Mark left his job to attend full-time, the\r\nhousehold would drop to Lisa's ~$35k while burning savings on both living costs\r\nand tuition. Six months of that could consume most of the $42k cushion. If he\r\nkeeps working and studies part-time, the money is safe but the timeline\r\nstretches "
- `e00138` · `corpus\doc_008.md` `/` [2480:2922]: "The most stabilizing thing a switching partner can offer is a pre-agreed\r\n*stopping rule*: \"If I haven't placed by month X, or savings drop below $Y, we\r\npull the ripcord and I take the fallback.\" This does two things. It caps the\r\ndownside the anxious partner is imagining (which is usually unbounded in their\r\nhead). And it reframes the switcher from \"person making a unilateral leap\" to\r\n\"person "
- `e00014` · `user_kb.md` `/` [3414:3766]: "What he has *not* clearly articulated, and what is worth probing: whether he\r\nwants to be a software engineer, or whether he wants to *not be a mechanical\r\nengineer*. These are not the same goal, and Mark has not separated them. He\r\nalso has not defined what \"success\" would look like 12 months out — is it a\r\njob offer, a salary number, a feeling?\r\n\r\n"
- `e00245` · `notes.json` `/21` [0:372]: "{\"content\":\"Honest 1am fear: what if I love coding as a hobby and hate it as a job? Hobbies don't have standups and Jira and a manager breathing down your neck about a sprint. Maybe the thing I actually love is that nobody's paying me to do it. How would I even test that before betting the family on it?\",\"date\":\"2024-05-01\",\"note_id\":\"n_022\",\"title\":\"What if I hate it\"}"
- `e00251` · `notes.json` `/27` [0:414]: "{\"content\":\"Coach-type question I can't shake: am I running toward software, or just running away from being bored in automotive? Because those lead to different plans. If it's 'toward,' a bootcamp makes sense. If it's 'away,' I might just be restless and a new job in any field would scratch it. Don't love that I can't answer this cleanly.\",\"date\":\"2024-06-01\",\"note_id\":\"n_028\",\"title\":\"Running "
- `e00253` · `notes.json` `/29` [0:387]: "{\"content\":\"Tried to count my real study hours this week: maybe 6, scattered, mostly after 10pm. At this rate self-study could take another two years to get job-ready, if I don't burn out first. That's the honest case against 'just keep studying on the side.' The slow path isn't risk-free either — it's just a different risk.\",\"date\":\"2024-06-12\",\"note_id\":\"n_030\",\"title\":\"Time audit\"}"
- `e00013` · `user_kb.md` `/` [3024:3414]: "- To do work that engages him intellectually the way coding currently does.\r\n- To increase his earning potential. He has friends in tech earning 1.5x to\r\n  2x his salary, and he is acutely aware of the gap.\r\n- To feel some control over his career trajectory rather than waiting for the\r\n  next reorg to decide his fate.\r\n- Not to blow up his family's financial stability in the process.\r\n\r\n"
- `e00109` · `corpus\doc_006.md` `/` [1898:2468]: "Midwest software salaries run below coastal numbers but so does the cost of\r\nliving, and the ratio is favorable. A first software role for a career changer\r\nin metro Detroit might land somewhere in the $70k-$95k range depending on the\r\nemployer and the candidate's portfolio; mid-level roles climb into the\r\nsix-figure range; senior roles comfortably exceed it. For someone currently\r\nearning in the "
- `e00024` · `user_kb.md` `/` [6259:6618]: "| Item | Amount |\r\n| --- | --- |\r\n| Mark base salary | $98,000 / yr |\r\n| Mark annual bonus | $5,000–$8,000 (variable) |\r\n| Lisa income (part-time) | ~$35,000 / yr |\r\n| Liquid savings | ~$42,000 |\r\n| 401k | Separate; treated as untouchable |\r\n| Mortgage | $1,750 / month |\r\n| Other significant debt | None |\r\n| Bootcamp option | $14,000 tuition, 6 months |\r\n\r\n"
- `e00016` · `user_kb.md` `/` [3784:4893]: "most of the childcare\r\n  load already. Any plan that further reduces Mark's availability at home has a\r\n  real cost that lands on her.\r\n- **Risk tolerance.** Mark is constitutionally cautious. A plan that is\r\n  financially sound but psychologically reckless (for him) is not actually a\r\n  fit, and vice versa.\r\n\r\n"
- `e00016` · `user_kb.md` `/` [3784:4893]: "- **Financial runway.** The family has roughly $42,000 in liquid savings (the\r\n  401k is separate and he considers it untouchable). The mortgage is\r\n  $1,750/month. A six-month, $14,000 bootcamp would consume both tuition and a\r\n  meaningful chunk of runway if he stopped working.\r\n- **Time.** Mark has a demanding full-time job and a three-year-old. His study\r\n  time is genuinely scarce — evenings "
- `e00109` · `corpus\doc_006.md` `/` [1898:2468]: "high $90ks in another field, the *first* tech job may be lateral\r\nor even a slight step down — but the slope afterward is steeper than in mature,\r\nslow-growth fields.\r\n\r\n"

Раундов: 1; model attempts: 21; время: 58.98 с.
