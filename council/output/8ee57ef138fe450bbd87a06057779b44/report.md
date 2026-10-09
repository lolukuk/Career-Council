# Отчёт совета пяти персон

Статус: **incomplete**

context_overflow: pinned closure

Режим: `model`. Режим выбранного LLM-провайдера. Формальное согласие не доказывает качество решения.

Вопрос: I'm thinking about switching careers from mechanical engineering to software development. Help me think through this decision.

Человек принимает итоговое решение после отчёта. Его выбор не меняет статус согласия персон.

Условный тестовый режим AI Tunnel. Превышения запрошенного лимита допускаются только до отдельного жёсткого потолка; этот профиль не предназначен для production.
Запрошено: 2000 токенов; потолок приёма: 8000; полученных ответов с превышением: 8.

Провайдер: `aitunnel`; модель: `gpt-6-luna-pro`; учёт контекста: `server_enforced`.

Reasoning effort: `none`. Эта настройка влияет на расход и качество модели; none используется для проверки процесса.

Предварительный count OpenAI ограничивает бюджет приложения, не подтверждает окно любой модели. AI Tunnel проверяет переполнение на сервере без точного предварительного count; сжатие отключено.

Лимит попыток относится к локальным запросам. Внутренние повторы провайдера и расходы после отмены неизвестны. Usage полученных ответов, включая отклонённые, сохранён в trace; отсутствующие данные не означают нулевой расход.

## Рекомендация и план

My position: do not quit or commit to the bootcamp now. Test software while employed, build and deploy a domain-specific project, and revisit the decision with Lisa after agreeing cash-flow and stopping guardrails and assessing fit and target-employer demand. Strongest counterargument: six scattered study hours weekly may mean years of slow progress and burnout; delaying is not risk-free, and the current job is not assuredly stable. The bootcamp might accelerate learning, but this dossier does not establish that it will lead to an offer or protect family finances.

Шаги:

1. First, discuss genuine buy-in and family capacity with Lisa; calculate household spending, minimum savings floor, and salary floor, and agree a stopping rule before any resignation or tuition.
2. If household capacity permits, set a sustainable, time-bounded employed trial; track actual study hours and whether work-like coding suits Mark.
3. Build and deploy one practical automotive/software project; seek feedback and investigate target employers' current hiring needs and compensation.
4. Reassess with Lisa against the agreed thresholds and evidence; consider training or switching only if the downside remains acceptable. Do not treat a project or trial as a job guarantee.

Альтернативы:

- Quit for full-time bootcamp now.
- Stay employed while testing software fit and building a domain-specific portfolio; revisit training after household guardrails and evidence are clear.

## Риски и условия решения

- The proposed employed trial may be feasible, but available study time, family capacity, and Lisa's agreement are not established; confirm them before setting a schedule.
- A shipped project and work-like trial may improve evidence of fit or hiring prospects, but neither guarantees an offer or salary; validate against target employers.
- A budget, salary floor, and stopping rule could bound financial risk, but no spending forecast or agreed thresholds are provided; determine these with Lisa before any resignation or tuition commitment.

Проверенная версия 1, digest `f1fbbef1783437fca88f44cc163aca9412660ad8168d6305f6485ed0f74bcb99`. Полный неизменный JSON решения сохранён в trace.json.

## Пять позиций и текущие оценки

### Peter Thiel

Build domain-specific software proof while employed; make the leap only when the family-backed downside is bounded.

Аргументы этого взгляда:

- What can you build at the intersection of automotive and software that a generic junior cannot? Ship that proof; credentials are no moat.
- Do not quit for the $14k bootcamp yet: the six-month income gap could consume much of savings.

Критерии:

- Switch only after Lisa's genuine buy-in, real six-month cash-flow and stopping rule, a shipped domain-specific project, and evidence software is the destination—not escape.
Контраргумент: Self-study at roughly six scattered hours weekly may take years; preserving income can quietly become permanent delay.

Оценка: **object** — The unfair-advantage thesis is domain-specific proof: what can Mark build at the automotive/software intersection that a generic junior cannot? The dossier supports exploring that thesis, not assuming it is already a moat. Credentials are not evidence of differentiation. The proposal's strongest case is its caution around savings, scarce time, and uncertain job fit; its strongest weakness is that a reversible trial can become unbounded delay. I would require a shipped project, work-like fit evidence, employer validation, and agreed household downside limits before a career switch. This proposal does not establish those conditions, so I object.

The proposal preserves the central distinction: domain knowledge may create an advantage, but credentials or a project alone do not establish hiring outcomes. Its employed trial is not itself an unfair advantage; the stronger thesis is to prove a specific automotive-software capability competitors lack. However, the proposal does not meet my blocking criterion: buy-in, a real six-month cash-flow plan, a shipped project, and evidence that software is the destination rather than an escape are still missing. The strongest counterargument is that staying employed and studying slowly may become indefinite delay and burnout. That argues for a defined, evidence-producing trial—not for treating unknown household capacity or market demand as settled.

### Warren Buffett

Stay employed while testing software and building a domain-led portfolio; defer bootcamp until downside is bounded.

Аргументы этого взгляда:

- A full-time bootcamp risks savings and income before hiring is assured.
- But endless part-time study risks burnout; domain-focused software work may offer a sharper route.

Критерии:

- Before leaving work or paying tuition: verify six-month cash flow and a savings/job-search stop rule with Lisa, and test whether software work—not escape from boredom—is the goal.
Контраргумент: The slow path may take years; a bootcamp could accelerate progress, while staying put risks continued disengagement.

Оценка: **object** — Circle of competence first: the dossier supports the downside figures and a potential automotive-software angle, not a reliable forecast of fit or hiring. Margin of safety requires the household cash-flow plan and Lisa's agreed stop rule before an irreversible commitment. The proposal sensibly delays quitting and recognizes the slow-path risk, but a recommendation to reassess later does not satisfy the criterion's required checks now. I object to approving this version; missing facts materially affect whether any transition is affordable or appropriate.

This exact proposal is cautious about quitting, but its required precondition—verify six-month cash flow and a savings/job-search stop rule with Lisa, and test whether software work is the goal—is not established. The proposal itself identifies missing household spending, Lisa's buy-in, a salary floor, and hiring conditions. The employed trial is also conditional on unconfirmed time and family capacity. The budget downside comes before any upside: bootcamp tuition and lost income could consume much of the savings cushion. A domain-led project may be useful evidence, not a hiring guarantee. I object rather than treating unknown safeguards as satisfied. Strongest counterargument: six scattered study hours weekly may make the employed route slow and raise burnout risk; that makes delay costly, but does not establish that quitting or bootcamp is safe.

### Robert Reich

Don’t quit yet: test software while employed, then decide with Lisa using real numbers and a clear exit rule.

Аргументы этого взгляда:

- The goal is growth without risking the family’s financial footing.
- Software has upside, but part-time study is slow and entry pay may fall short.

Критерии:

- Choose a bounded trial only after Lisa’s genuine buy-in, cash-flow and salary floors, and a stopping rule are explicit; test job-fit and hiring conditions before quitting.
Контраргумент: Staying employed feels safer, but six scattered study hours weekly may prolong the transition and burnout; the current job is not immune to layoffs.

Оценка: **object** — My position is to object to this exact version, not to reject a software transition categorically. A reversible trial can be sensible, but household consent, family capacity, financial floors, and stopping conditions must be real prerequisites, not future tasks after the trial begins. The strongest counterargument is that six scattered hours weekly may prolong the transition and create burnout; delay is not risk-free, and the current job is not assuredly stable. Still, the record does not establish what target employers offer in income, benefits, hiring conditions, or bargaining power, or that a bootcamp would improve those outcomes. The proposal's own caveats acknowledge key unknowns, so they cannot be treated as satisfied.

This is the initial immutable proposal (version 1); there is no prior draft to compare. I support testing software without quitting immediately, but the recommendation and steps do not meet my blocking criterion: they say to agree guardrails and investigate hiring conditions, yet proceed to a trial before Lisa’s genuine buy-in and actual cash-flow, salary-floor, stopping-rule, and employer-offer details are established. The slow-study and burnout counterargument is real, but does not establish that a bootcamp improves hiring outcomes or that the household can bear the transition. Who bears the cost is clear: Lisa already carries most childcare, and leaving work could shift income risk to the family. Benefits, healthcare, and actual hiring terms are not established; ask target employers what they offer before treating demand as evidence. The cited claims about goals, finances, limited study time, job-fit uncertainty, and a possible domain-led project are supported. This proposal does not claim a job is guaranteed. Object to this exact version; do not infer that agreement or feasibility is already established.

### Nassim Nicholas Taleb

Preserve income and runway; run a reversible software trial before any resignation or tuition bet.

Аргументы этого взгляда:

- Keep the paycheck; don't quit for bootcamp now. Tuition plus lost income could consume the cushion.
- But don't mistake delay for safety: build and deploy a domain-led project, test coding as work, and network while employed.

Критерии:

- Switch only with Lisa's genuine buy-in, a household-agreed savings/job-search stopping rule, a viable salary floor, and evidence of job-fit and hiring demand.
Контраргумент: Self-study is slow at about six hours weekly; delay risks burnout and lost momentum, while the current job is not guaranteed stable.

Оценка: **object** — The proposal is directionally prudent, but approval requires the exact compound criterion to be established. It is not: key household consent, financial thresholds, and market/fit evidence are missing. The dossier supports both sides: quitting risks substantial runway, while slow study and possible burnout make delay costly. Preserve optionality, but do not present the current plan as satisfying the stated switch criterion.

The proposal's central recommendation is cautious and reversible, but its mandatory criterion is not established: the dossier lacks Lisa's confirmed buy-in, agreed stopping rule and salary floor, and evidence of fit and hiring demand. The proposal itself acknowledges these gaps, so they cannot be treated as satisfied merely because it recommends obtaining them later. I object to approving this version as a decision-ready recommendation; its strongest counterargument is also real: part-time study has been only about six scattered hours weekly, creating delay and burnout risk.

### Marcus Aurelius

Test the path while employed; decide on evidence and shared guardrails, not fear or salary envy.

Аргументы этого взгляда:

- Pursue software as a bounded experiment, not a leap: protect income while testing fit and building a portfolio.
- Keep the current job for now; use a sustainable study rhythm and low-cost, work-like software trials before choosing training.

Критерии:

- Choose a switch only after Lisa's genuine buy-in, a household budget/runway and salary floor, a shipped portfolio project, and evidence software work fits; agree a stopping rule.
Контраргумент: Six scattered study hours weekly may make self-study drag on and risk burnout; delay also has a cost.

Оценка: **object** — The controllable next actions are to discuss capacity with Lisa, establish numbers and a stopping rule, and test fit through sustainable practice and a deployed project. Status anxiety or salary comparison does not establish that a switch is wise; nor does caution make slow progress harmless. The strongest objection to my position is that six scattered hours weekly may prolong the path and risk burnout. Still, the compound criterion is unmet, so I object rather than treat unknown conditions as satisfied.

The proposal aligns with my original position: preserve income for now, test software through practical work, and make a later decision with Lisa and agreed guardrails. It also carries forward the main counterargument that limited study time makes delay costly. However, my blocking criterion requires all specified evidence before a switch: Lisa's genuine buy-in, a household budget/runway and salary floor, a shipped portfolio project, evidence of work-fit, and an agreed stopping rule. The proposal correctly identifies these as missing and makes them prerequisites; they are not established as satisfied. Thus I support the cautious interim direction, but not an unconditional approval of this version as fulfilling that criterion.

## Возражения и противоречия

- o1 / Peter Thiel: Do not treat the employed trial as approval to switch or set a schedule: my blocking criterion requires genuine family buy-in and bounded six-month cash flow, a shipped domain-specific project, and evidence software is the destination rather than escape. The dossier leaves these unresolved; build the evidence before reconsidering a leap. (pending).
- o2 / Warren Buffett: The deciding criterion warren_buffett/c1 is unmet: cash-flow and stop-rule verification with Lisa, and evidence that software work—not simply escape from current work—is the goal, are not established. Do not approve a transition or tuition commitment on this record. (pending).
- o3 / Robert Reich: The blocking criterion is unmet: the plan calls for an employed trial before establishing genuine household buy-in and explicit financial guardrails, and does not yet establish employer hiring terms. Lisa already bears substantial childcare load; the proposal must not treat her capacity or consent as assumed. (pending).
- o4 / Nassim Nicholas Taleb: The proposal advises a software trial while employed, but its own criterion requires established buy-in, shared downside limits, a viable salary floor, and evidence of fit and hiring demand before switching. Those conditions remain unknown; do not treat a later reassessment as satisfying them now. (pending).
- o5 / Marcus Aurelius: My blocking criterion is not satisfied: essential household and career evidence remains missing. The recommendation appropriately defers quitting, but the proposal cannot establish readiness for a switch; keep that decision conditional on every stated guardrail and fit test. (pending).

## Недостающие данные

- Lisa's genuine buy-in and home bandwidth
- Six-month cash flow and minimum savings floor
- Job-fit test and 12-month success definition
- Six-month household cash-flow plan and minimum savings floor.
- Lisa's genuine buy-in; software-work fit; target first-job salary floor.
- Household spending and cash-flow forecast
- Lisa's buy-in and acceptable risk
- Target employers' pay, benefits, hiring terms
- Lisa's genuine buy-in and agreed runway floor
- Monthly spending and minimum acceptable salary
- Evidence of job-fit and current hiring demand
- Lisa's genuine agreement and family capacity
- Household spending, acceptable salary floor, and runway threshold
- Experience of software work as a job, not a hobby
- Lisa's genuine buy-in and family capacity; household spending and savings threshold; acceptable salary floor; target-employer hiring conditions; definition of 12-month success.

## Источники и границы проверки

Загружено источников: 90; показано моделям: 35; chunks: 52.
Полный inventory, поисковые ранги, версии, голоса и происхождение цитат сохранены в trace.json.
Исходные даты досье не подтверждают актуальность сведений. Проверка substring не доказывает смысловую поддержку вывода.

- `e00113` · `corpus\doc_006.md` `/` [3009:3506]: "The market is tougher than 2021 but far from closed, and the region offers a\r\nspecific edge: the overlap between traditional engineering/automotive domain\r\nknowledge and software demand. A candidate who can credibly say \"I understand\r\nboth how this physical product works *and* how to build the software around it\"\r\nis solving a hiring problem that pure-software juniors can't. That is a sharper\r\n"
- `e00249` · `notes.json` `/25` [0:381]: "{\"content\":\"If I'm going to convince anyone to hire me, the expense tracker isn't enough. Need one real, polished, deployed project that solves an actual problem. Maybe something using my automotive domain knowledge — a parts/inventory tool? Lean into the thing I already know instead of pretending I'm a fresh grad.\",\"date\":\"2024-05-16\",\"note_id\":\"n_026\",\"title\":\"Portfolio idea\"}"
- `e00016` · `user_kb.md` `/` [3784:4893]: "- **Financial runway.** The family has roughly $42,000 in liquid savings (the\r\n  401k is separate and he considers it untouchable). The mortgage is\r\n  $1,750/month. A six-month, $14,000 bootcamp would consume both tuition and a\r\n  meaningful chunk of runway if he stopped working.\r\n- **Time.** Mark has a demanding full-time job and a three-year-old. His study\r\n  time is genuinely scarce — evenings "
- `e00025` · `user_kb.md` `/` [6618:7151]: "The headline tension: the bootcamp's $14k tuition is affordable on paper, but\r\nthe family's margin is thin. If Mark left his job to attend full-time, the\r\nhousehold would drop to Lisa's ~$35k while burning savings on both living costs\r\nand tuition. Six months of that could consume most of the $42k cushion. If he\r\nkeeps working and studies part-time, the money is safe but the timeline\r\nstretches "
- `e00253` · `notes.json` `/29` [0:387]: "{\"content\":\"Tried to count my real study hours this week: maybe 6, scattered, mostly after 10pm. At this rate self-study could take another two years to get job-ready, if I don't burn out first. That's the honest case against 'just keep studying on the side.' The slow path isn't risk-free either — it's just a different risk.\",\"date\":\"2024-06-12\",\"note_id\":\"n_030\",\"title\":\"Time audit\"}"
- `e00013` · `user_kb.md` `/` [3024:3414]: "- To do work that engages him intellectually the way coding currently does.\r\n- To increase his earning potential. He has friends in tech earning 1.5x to\r\n  2x his salary, and he is acutely aware of the gap.\r\n- To feel some control over his career trajectory rather than waiting for the\r\n  next reorg to decide his fate.\r\n- Not to blow up his family's financial stability in the process.\r\n\r\n"
- `e00109` · `corpus\doc_006.md` `/` [1898:2468]: "Midwest software salaries run below coastal numbers but so does the cost of\r\nliving, and the ratio is favorable. A first software role for a career changer\r\nin metro Detroit might land somewhere in the $70k-$95k range depending on the\r\nemployer and the candidate's portfolio; mid-level roles climb into the\r\nsix-figure range; senior roles comfortably exceed it. For someone currently\r\nearning in the "
- `e00245` · `notes.json` `/21` [0:372]: "{\"content\":\"Honest 1am fear: what if I love coding as a hobby and hate it as a job? Hobbies don't have standups and Jira and a manager breathing down your neck about a sprint. Maybe the thing I actually love is that nobody's paying me to do it. How would I even test that before betting the family on it?\",\"date\":\"2024-05-01\",\"note_id\":\"n_022\",\"title\":\"What if I hate it\"}"
- `e00024` · `user_kb.md` `/` [6259:6618]: "| Item | Amount |\r\n| --- | --- |\r\n| Mark base salary | $98,000 / yr |\r\n| Mark annual bonus | $5,000–$8,000 (variable) |\r\n| Lisa income (part-time) | ~$35,000 / yr |\r\n| Liquid savings | ~$42,000 |\r\n| 401k | Separate; treated as untouchable |\r\n| Mortgage | $1,750 / month |\r\n| Other significant debt | None |\r\n| Bootcamp option | $14,000 tuition, 6 months |\r\n\r\n"
- `e00014` · `user_kb.md` `/` [3414:3766]: "What he has *not* clearly articulated, and what is worth probing: whether he\r\nwants to be a software engineer, or whether he wants to *not be a mechanical\r\nengineer*. These are not the same goal, and Mark has not separated them. He\r\nalso has not defined what \"success\" would look like 12 months out — is it a\r\njob offer, a salary number, a feeling?\r\n\r\n"
- `e00254` · `notes.json` `/30` [0:629]: "{\"content\":\"Funny thing: I've asked maybe five people and gotten five answers. Raj says just leap. Dave basically thinks the question is crazy. Lisa wants a plan, not a feeling. The finance guy at the gym said the bootcamp's fine on paper but I'd be betting the emergency fund on a timeline I don't control. They're all kind of right, which is useless. Nobody's weighing the same thing — upside, "

Раундов: 1; model attempts: 29; время: 103.44 с.
