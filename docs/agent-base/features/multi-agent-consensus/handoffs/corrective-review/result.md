# Independent actual review — C02–C05

2026-10-09. Reviewer: /root/route_review. Final engineering/code verdict: **PASS**, C-R01 independently closed; scale and author full-suite evidence reviewed. Final semantic/full-product verdict: **BLOCKED** after the third/final authorized live run. Initial code verdict was **BLOCKED** and its finding/evidence are preserved. Runtime/source files were read only; no paid calls, provider changes or extra agents. Historical scripted acceptance is preserved and does not close original-assignment acceptance.

## C-R01 / P2 — get_tasks returns detail evidence instead of inventory scope

Verified `council/task_tools.py:26–40`: records returned for `get_tasks` contain only inventory fields, while evidence contains every chunk of the corresponding `get_task_details` sources. The tool therefore exposes detail-only information before a hierarchical detail request and pins all these detail chunks in the advisor context (`council/context.py:57`). This violates the reviewed scoped-record/evidence contract and unnecessarily increases the pinned payload. The inventory is also reconstructed from detail responses rather than retaining the actual successful API inventory response.

Independent reproduction using existing test fixtures: the inventory response is `[{"task_id":"t1"}]`, but returned evidence is `{"description":"Plan","task_id":"t1"}`. An assertion that inventory evidence excludes detail-only description fails, exit 1. This is a confirmed behavioral failure, not an environmental test failure.

Required correction: retain the frozen successful `get_tasks` inventory observation with its own valid provenance/evidence, or provide exact scoped inventory excerpts that cannot expose extra detail fields. `get_task_details` must retain its separate detail evidence; `get_subtasks` must remain scoped to the selected parent. Do not merely remove description from records while returning the same unrestricted evidence.

## Checked without further findings

- Note shortlist is bounded to 20 IDs, unknown/duplicate selections fail, valid empty selection is distinct from failed filtering. Selected-note IDs are prioritized and optional noise is excluded; transitive cited counterevidence remains pinned.
- All five personas have typed read-action access, arguments/IDs are checked, reads are bounded to three per advisor, observations are advisor-local, and dispatch operates on API-captured data without re-fetching or reading private JSON files.
- Repair requests have fresh request identity and changed payload digest, retain base request reference, and carry fixed validation codes rather than raw exception/model output. Context bytes are checked before dispatch; attempts/time/cancellation and the existing exact-citation/consensus guards remain enforced.
- Human-readable report uses recorded DTO content, preserves partial-barrier honesty and dissent, and retains exact decision JSON in trace. README documents architecture, rationale, future work and the distinction between historical acceptance and full-product acceptance.

## Independent checks

`.\\.venv-consensus\\Scripts\\python.exe -m pytest council/tests/test_corrective.py council/tests/test_context.py council/tests/test_model_boundary.py -q` — **21 passed in 1.17s**, exit 0.

The independent inventory-scope reproduction described above — **failed assertion**, exit 1. Existing fixture tests do not currently catch this difference between records and evidence.

Root full suite and scale execution were running at review time; their results are not attributed to this reviewer. Live answer quality, persona contrasts and semantic citation support remain pending actual live artifacts.

## C-R01 independent closure — 2026-10-09

`Sources` now captures the validated successful API inventory as `tasker:inventory`, origin `tasker:get_tasks`, before the detail loop (`council/sources.py:104–111`). `SnapshotTools` uses only `tasker:get_task_details` sources for detail lookup; inventory dispatch returns the actual frozen inventory and only inventory evidence (`council/task_tools.py:17–28,36–39`). Empty successful inventory remains an explicit `[]` observation rather than disappearing.

Own reproduction now passes, exit 0: inventory records `[{"task_id":"t1"}]`, inventory evidence origin `tasker:get_tasks` and text `[{"task_id":"t1"}]`; no description appears. A separate detail dispatch still returns description evidence. **C-R01 closed.**

Own affected check `.\\.venv-consensus\\Scripts\\python.exe -m pytest council/tests/test_corrective.py council/tests/test_context.py council/tests/test_retrieval.py council/tests/test_sources.py -q` — **23 passed in 0.55s**, exit 0.

Also inspected the measured-failure-driven retrieval delta: optional context admission balances existing source-type pools while preserving within-type ranking (`context.py:72–92`); excluded notes remain excluded, transitive pinned evidence and serialized byte checks are retained. Initial retrieval weights the original question 3 and each expertise query 1, records that weight in coverage, and keeps unweighted later feedback searches (`runtime.py:390,523`; `retrieval.py:163,203`). No schema/citation normalization, increased budget or provider/model change was introduced. These code changes are acceptable; gold-hit/scale effectiveness must still be demonstrated by the pending actual scale run, not inferred from the heuristic.

## Post-live1 context/retrieval delta review — 2026-10-09

Code verdict remains **PASS**. Tool names/instructions are now included in `build_context` before measured optional admission (`context.py:31–36`); `read_tools` no longer appends unmeasured metadata afterward (`runtime.py:412–418`). Advisor-local tool observations carry records and `evidence_ids` rather than duplicating complete evidence in payload (`context.py:28–30`); exact tool evidence is still pinned and appears once in the main evidence list. The typed action/ID checks, max3 read limit, source provenance, exact quote checks, attempt deadlines and mandatory serialized-request gate remain unchanged. Compact initial-stage target is a prompt preference, not a DTO or budget relaxation.

Note shortlist now reserves at most five lexical hits inside the existing overall 20-item shortlist (`retrieval.py:205–208`). Hybrid results, primary-question weight and bounded model selection remain in place; shortlisted noise cannot bypass the selection validation/context filter.

Own affected command `.\\.venv-consensus\\Scripts\\python.exe -m pytest council/tests/test_corrective.py council/tests/test_context.py council/tests/test_model_boundary.py council/tests/test_cli_report.py -q` — **26 passed in 1.43s**, exit 0. This includes allow-list/foreign-ID rejection, advisor isolation, repair identity, timeout/late cancellation, report fidelity and source scope. No additional adversarial tool/report safety finding was identified in this delta.

Independently inspected saved scale metadata `council/output/scale-465e90dacfd54ddc9dc6d20f9d03791c/metadata.json`: PASS, 1200 documents/300 notes, gold positive and negative document/note hits present, no selected noise, serialized request 28581 bytes, elapsed 13.0852s, sampled process-tree RSS 650608640 bytes. Mode is explicitly `scripted_filter_fixture` with actual dense retrieval and no paid calls; this evidence proves the measured search/context path, not live semantic filtering or all-stage discussion size. Final lexical-lane scale repeat was pending when inspected.

Independently inspected live1 saved trace `ec65ba6a1f88475780cdecc8881f4ee6`: `incomplete`, `complete serialized request byte budget`, 10 attempts/usage records, five tool dispatches, zero atomic positions and zero decisions. This failure is preserved; the sizing repair is justified by the actual failed path. A running second paid attempt is not a successful artifact. Live semantic review and final original-assignment acceptance remain pending.

## Post-live2 compact-projection independent review — 2026-10-09

**Contract/code verdict: PASS; no dispatch blocker found.** The model evidence projection omits only backend audit fields `digest`, `source_digest`, `start`, `end`; complete `text`, source/chunk IDs, section, origin and location remain unchanged (`context.py:70–76`). The immutable registry and trace retain audit metadata. `validate_citations` still checks shown chunk IDs, backend chunk text digest and exact contiguous quote (`context.py:8–16`). No quote, factual text, Position/Proposal/Vote schema, pinned counterevidence, output/context cap or consensus condition is relaxed. Coordinator roster is compacted to IDs/names while receiving all five full positions; each advisor receives its complete own frozen framework at initial/review (`context.py:38–49`). This is an acceptable input projection rather than a changed evidence contract.

Own affected check `.\\.venv-consensus\\Scripts\\python.exe -m pytest council/tests/test_context.py council/tests/test_corrective.py council/tests/test_model_boundary.py -q` — **23 passed in 1.24s**, exit 0. Root separately reports exact whole suite **133 passed in 29.27s**, exit 0; this is author evidence, not a reviewer rerun. The approved third/final full paid run may proceed after that check within unchanged limits; success is not guaranteed and no additional paid diagnostics are authorized by this review.

Live2 `e7af238a4d1d48bdb83af33a1079ea4d` independently inspected: five valid atomic positions, 13 actual read dispatches, 22 attempts, no decision; terminal `incomplete` / `context_overflow: pinned closure`. Failure history remains preserved. The saved five positions were independently parsed as strict JSON DTOs and all **28 citations** revalidated against each owner's accepted request evidence IDs and registry exact-quote/digest checks; exit 0.

Semantic partial review: the five positions give useful source-grounded reasons to retain income while testing an automotive-domain project, budget household runway, seek Lisa's genuine agreement and test coding-as-work. Cited savings of $42k, partner income about $35k, scarce approximately six-hour study time, bootcamp downside and automotive/software overlap are supported by shown profile/documents/notes. No invented achieved financial benefit or guaranteed hiring outcome was identified. Recommendations are analysis/inferences rather than arithmetic proof of affordability.

**FR-1 contrast remains a quality caveat:** recommendations and tone are very similar across all five. Thiel's credential-versus-domain-edge emphasis, Taleb's bounded-downside emphasis and Buffett's financial caution are present, but Reich and Marcus largely repeat generic staged-transition advice. These five initial responses do not alone demonstrate five strongly recognizable contrasting personalities. No common decision or visible final integration exists yet, so FR-2/FR-3 and full-product acceptance remain pending the final artifact and independent semantic review.

## Final pre-live3 persona-policy delta — 2026-10-09

**PASS; no identity/context/contract blocker.** The short `PERSONA_VOICES` cues use the supplied perspectives without adding dossier facts or a new runtime persona. They apply only to initial/review stages. `Council` copies the cue and stage-hint maps at initialization, includes both in `snapshot_id` and trace, and uses the same `stage_policy` in measured context construction and actual model request (`runtime.py:149,153–156,185–207`). Exact quotes, validated DTOs, visible evidence, vote conditions and all numeric budgets remain unchanged. Prompt wording is not proof that the resulting five voices meet FR-1.

Own command `.\\.venv-consensus\\Scripts\\python.exe -m pytest council/tests/test_context.py council/tests/test_model_boundary.py -q` — **13 passed in 1.03s**, exit 0. Root separately reports full suite **133 passed in 12.94s**, exit 0. This safe policy delta and the previously approved compact projection permit the third/final already-authorized full run; no fourth paid run or extra paid diagnostic is approved. Full semantic review still waits for the terminal artifact.

## Final independent actual review — live3/3 and final scale

**Engineering/code PASS; original-product acceptance BLOCKED.** Final trace `council/output/1100b8f39a594601af28e5fa7ccd25ba/trace.json` independently inspected: `failed`, 38.5971s, 23 attempts, zero committed positions/decisions. Thiel, Taleb and Marcus have individually accepted initial events. Buffett's two attempts fail `citation_quote_not_exact`; Reich's first fails the same guard and his repair is cancelled after the sibling failure. The atomic barrier correctly rejects partial initial completion. This is technical failure before discussion, not `no_consensus` or a completed five-expert answer.

Independent read-only artifact assertions passed, exit 0: all 23 attempt IDs match usage rows, with one cancelled cost retained as unknown; maximum serialized request **29952 bytes** is below 32768; both repairs have new IDs with original base references. **11 model-selected snapshot dispatches**, at most three per persona: all five use `get_tasks`, all five use `get_task_details(t_002)`, and Reich also reads `t_010`. Inventory evidence has actual `tasker:get_tasks` provenance. These are distinct from **22 physical API attempt events**, including a transient retry, not 11 fresh external API calls.

Shortlist contains **20** valid IDs; **15** are selected. Initial contexts contain no unselected note. Selected notes concern career motivation, a real transition anecdote, household affordability, learning, hiring/age concerns, layoffs, partner concerns, market comparisons, job-versus-hobby fit, alternative promotion and domain portfolio. No obvious unrelated household/advertising note was selected; this finding applies to this mock case, not arbitrary note distributions. Raw rejected/cancelled output is deliberately absent, so the particular erroneous quote cannot be reconstructed. The three individually accepted but uncommitted Position payloads are also absent from `initial_positions`; their contents cannot be independently reassessed from this artifact. Earlier live2 five-position semantic evidence remains separate and does not substitute for a final answer.

Final scale `council/output/scale-73855c2e7c4f4bcea3cd24ea77966fd4/metadata.json` independently inspected: **PASS**, 1200 documents/300 notes, positive/negative gold document/note hits present, no selected noise, **22906-byte** initial request, **14.7127s**, sampled parent RSS **135946240** / process-tree RSS **650575872** bytes. Actual dense model and explicit deterministic/scripted relevance fixture are used. This establishes measured retrieval/context capacity, not live relevance quality or later discussion-stage admission.

Author exact suite **133 passed in 12.94s**, exit 0, is author evidence; reviewer focused checks and independent artifact assertions above are separate. No remaining engineering finding was identified in C-R01 closure or safe projection/policy deltas. FR-1 live personality contrast and FR-2/FR-3 full common helpful result remain **not accepted**, because no final five-position/proposal artifact exists. No fourth paid run or extra paid diagnostic; quote normalization, budget expansion and replacement of failed output are not authorized by this completed route. Original-product acceptance remains open, historical scripted acceptance and all three failed artifacts preserved.
