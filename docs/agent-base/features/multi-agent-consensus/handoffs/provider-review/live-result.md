# Narrow live-boundary correction review

2026-10-09. Reviewer: consensus_design_review; implementation/live author: root. User explicitly authorized continued bounded live work. Reviewer reads no raw.env/keys and makes no paid/provider requests.

**Current checkpoint:** PI08 focused diagnostic implementation review PASS; PI08-R01/P3 closed. Runtime/context diagnostic full123 passed24.62s; final report wording regression1 passed0.93s after the copy-only correction. Fresh Robert single-position diagnostic passed one attempt; previous full council f03 remains FAILED with no atomic five-position barrier/decision/consensus. PI07 PASS/history preserved. Checks are completed, not running; earlier pending/BLOCKED notes below are history. This is not five-person live-quality certification or successor user acceptance.

## Offline delta verdict: PASS; corrected live outcome pending

Actual providers.py prepares upstream_provider from the selected public catalog entry, records it with context/max_output metadata in the run snapshot, and selects exactly one wire field: OpenAI upstream → max_completion_tokens; other upstream → max_tokens. Both receive the unchanged frozen Request.output_tokens (default2000). No model-name guessing, fallback, cap increase, reasoning setting or model substitution was added.

Actual test_catalog_selects_output_cap_field exercises openai/anthropic metadata, asserts2000 and exclusive field presence. The3753-token overbudget negative fixture exists for both adapters. Actual generation still rejects counts[1] > request.output_tokens before output admission; rejected usage remains captured. Existing schema/citation/consensus/deadline guards remain authoritative.

Author current full evidence: `.venv-consensus/Scripts/python.exe -m pytest council/tests -q` → exit0,107 passed12.17s, session92594. Reviewer inspected changed code/fixtures rather than rerunning the already green full suite. No material delta finding.

## First live failure and causal uncertainty

Author-reported preserved artifact: council/output/b76e097ba55746d382d29ce3cb245617. AI Tunnel gpt-6-luna-pro returned matching model, input29295/output3753, reported cost_rub0.82, with max_tokens2000 sent. Run failed provider_output_token_budget: five initial local dispatches, no accepted positions or decision. This demonstrates connectivity and output guard refusal, not successful protocol completion or bounded remote spending. Usage of incomplete/cancelled parallel calls may remain unknown.

[Official AIT parameters](https://aitunnel.ru/docs/parameters), checked in this dispatch, documents max_completion_tokens for newer OpenAI models AND automatic max_tokens forwarding on the direct newer-OpenAI route. Therefore explicit modern field is a viable compatibility correction; the original3753 result's cause is **not established** solely by this replacement. Neither catalog nor offline fixtures prove the gateway honors the cap.

Root's next evidence: one authorized synthetic cap probe without dossier; corrected full run only if that succeeds. Do not retry five-dispatch runs blindly or relax local cap/guards to claim success. A probe can demonstrate observed enforcement for that selected route/request, not universal arbitrary-model accounting or live reasoning quality.

Current reviewer activity: narrow code/fixtures/docs review and official documentation browse only. First failed artifact/history retained. Await actual authorized probe/corrected live evidence; no final live-success claim or successor acceptance here.

## Actual probe and second default-profile failure

Author supplied synthetic no-dossier probe: PASS,61 output tokens, reported cost0.04 rubles. Subsequent full run648fa815b0bd48e6897f6aa21e7bc9a6 still failed provider_output_token_budget: output3692, reported cost0.81, no positions/decision, first five dispatches. Thus the modern cap-field substitution **did not resolve** the observed full-request overbudget. The successful small probe cannot certify enforcement for full payloads. Both failed artifacts remain history, guards did not accept overbudget answers.

## Optional explicit effort delta — offline PASS, live none outcome pending

Actual Settings is frozen, effort validated against finite allowed values, CLI>environment>file, omitted/blank gives None. No user model/default effort/key change in code. A selected effort is inserted by the common _wire into both OpenAI count and generation and AIT request. It participates in model snapshot digest, trace, preparation trace and report; default omits the wire reasoning field. Existing caps/deadlines/DTO/citation/unanimity guards remain.

Read actual settings/main/providers/runtime/report and effort precedence/default omission fixtures. Author current full:110 passed11.98s exit0/session67455. No new material code finding; no broad rerun by reviewer.

[AIT reasoning](https://aitunnel.ru/docs/reasoning) explicitly documents Luna none support and distinction between mode and effort. [OpenAI input count reference](https://developers.openai.com/api/reference/resources/responses/subresources/input_tokens/methods/count) includes reasoning configuration. These are supported option semantics, not assurance every model accepts every enum or that none improves decisions. Unsupported selection remains terminal, no fallback.

Author now runs the same selected gpt-6-luna-pro with explicit `--reasoning-effort none` as a process profile. Any future success must be attributed to that profile and observed run, not default-pro success, universal cap enforcement or independent semantic-quality certification. Reviewer made no authenticated/count/generation calls and inspected no credentials. Live outcome pending.

## Third full run and bounded-prompt delta

Author-reported none-profile run c354b3d8ab1c4b2fa74495e39819bb59 failed output cap as well: output2212, reported cost0.68, no accepted positions/decision. The guard2000 remains. None support and profile provenance did not establish full-request cap enforcement or successful discussion; the previous pending outcome above is superseded by this failure.

Reviewed actual prompts.bounded_policy and runtime integration. No material inspection finding: prompt states total output budget including reasoning and aims for visible JSON below half; explicitly forbids omission of required fields/check IDs, objections/conflicts, negative evidence and necessary qualifications, and forbids approval for brevity. Base independence, assumption/caveat, exact-version and counterargument instructions remain. Half-budget target is an instruction/heuristic, not a certified tokenizer or guarantee of semantic preservation.

Council captures policy once, uses the same string for complete serialized Request measurement and call/retry, records policy_digest in snapshot and trace. Evidence context construction, DTO/reference/citation/consensus guards, output cap and roster are unchanged. Review drafts with many claims/checks may be unable to fit; the intended safe result remains refusal/invalid/exhausted, never dropping checks or manufacturing consensus.

Current delta full suite session55794 still pending at this review entry; **inspection has no blocker, final offline PASS awaits current full exit0**. Root plans one exact-dossier Nassim initial-position diagnostic through existing Council.call, with real Position/citation/criterion checks, max2 and45s; it is not a five-person decision, review round or consensus. Do not generalize its outcome to later full discussion or live-quality certification. Reviewer performs no paid calls or product edits.

## Prompt closure and transport-bounds descriptions — offline PASS

Prompt-delta pending55794 is closed by author current full exit0,110 passed88.05s. Its subsequent single Position call received1622/1587 tokens but neither response passed DTO validation. A following single diagnostic metadata artifact live-validation-936f03f3a0ee447fbe87b3f5643da400 was independently read: output1655, schema layer, criteria/too_long, reported cost0.58. Short output was insufficient for a valid Position.

Reviewed current transport_schema: recursive node descriptions now include original min/maxItems, min/maxLength and numeric lower/upper bounds. Criteria1–4, homogeneous tupleexact2 and quotation max400 remain model-visible even when transport keywords are omitted for compatibility. Original local DTO, bounds, cardinality and restore_defaults are unchanged and remain decisive. Existing original description is retained. No new unsupported enforcement keyword is emitted; these instructions are hints, not strict provider validation.

Both count and generation build the same deterministic normalized schema from the frozen original Request.response_schema_json. Expanded schema still passes the existing wire-body cap; complete Request/output/deadline/consensus/citation guards and default None effort remain. Actual assertions cover criteria1–4, exact2 tuple and quote400 alongside existing local tuple rejection.

**Current offline delta verdict: PASS**, no material inspection finding. Author current full after bounds descriptions:110 passed31.27s exit0/session87798. No redundant broad suite was run by reviewer.

Following single diagnostic live-validation-b942c4bdc1db4eaa8ccdc10c8db8b64a metadata independently read: output1788, reported cost0.6, failed/citation_or_transport ValueError, no accepted Position. Author reports schema passed; metadata alone narrows only to the recorded citation_or_transport layer and does not prove a specific quote/chunk cause. Root's next bounded diagnostic may locate the exact category while keeping schema-valid diagnostic artifacts explicitly unaccepted. Successful live Position/discussion/consensus and semantic quality remain unproven; default-pro overbudget history remains unresolved.

## Existing strict live checkpoint — review closed honestly

Read current provider-live-verification, README current outcome, appended workflow/status/routing/provider-verification evidence, synthetic smoke metadata and final diagnostic metadata. Independently filtered three preserved full traces: each status failed, five attempts, zero initial_positions/decisions; observed outputs3753/3692/default and2212/none. Synthetic metadata confirms61-token successful tiny request. Final diagnostic1e9d02c0bdd84313a007e3baa603ac62 confirms failed/transport/provider_output_token_budget,2015>2000, input28887, reported cost0.47, none, one dispatch. It did not reach DTO validation, so prior1788 ValueError cause remains unknown.

No current checks falsely running, no live consensus/quality or default-pro success claimed. Code/offline110 passed31.27s checkpoint PASS, observed full live outcome FAIL. Other cancelled charges remain unknown. Direct OpenAI live unrun; no cross-provider key fallback. No additional product correction from this closure. Author has stopped unchanged paid retries; failed artifacts and accepted original prototype remain preserved.

## PI07 independent design AND plan review — PASS

New direct user steering allows an AIT test-only accounting exception; it does not authorize relaxing evidence or consensus. Reviewed concrete provider-design.md §PI07. Design PASS; serial plan PI07a→b→c→d PASS. No material documentary blocker. This supersedes the previous need to choose another provider/model for the next authorized test; it does not convert prior failures into successes or certify future implementation.

Adversarial boundaries are explicit: requested wire cap remains2000; only opt-in mode=model + AIT/server_enforced/reliable=false may admit reported output2001–8000 to ordinary validation.8001 must reject; missing/noninteger/negative usage, refusal/truncation/model mismatch still reject. DefaultAIT and every directOpenAI/custom strict adapter retain requested cap. Wrong-provider CLI/library flag must fail before dossier disclosure. A single shared effective-ceiling helper must govern BOTH provider and Council output checks, avoiding either inconsistent acceptance or global relaxation.

Snapshot/trace must identify frozen test policy and ceiling; per-attempt requested cap/excess flag preserve actual usage, including rejected responses, with unknown counts represented as null. Report marks conditional AIT testing, not production/exact accounting;8000 is an acceptance boundary based on reported counts, not a remote cost/context/termination guarantee. Partial larger positions may still cause pinned context overflow or DTO/citation failure; these remain legitimate terminal outcomes, never excuses to omit obligations/check IDs/negative evidence or autoapprove.

Plan uses one root implementer, existing reviewer and existing fixtures/full suite, no new infrastructure/agents. Explicit negatives cover defaults/OpenAI/excess>8000/flag/usage/refusal/citation/consensus; actual profile and excess reporting checked before one bounded full live attempt. Actual independent final review after evidence remains required. User steering provides authorization for this scoped test exception; reviewer adds no repeat approval gate. Historical110 green is pre-PI07 evidence and cannot certify new code. Reviewer made no paid calls, product edits or key access.

## PI07 actual implementation review and live evidence

Read actual Settings bool/AIT-only constructor+loader checks, early CLI scripted/OpenAI rejection, capability admission, shared output_token_ceiling in provider and Council, unchanged wire2000, unconditional usage/type/refusal/model/DTO/citation/consensus validation, profile snapshot/preparation/trace/report and existing fixtures. Normal AITtest3753 protocol scenarios and8000/8001 boundary are covered. Author current full:117 passed33.30s exit0/session38599. No output-admission or consensus bypass found in these paths.

Independently filtered new live trace24399613e83e4ecf9c1561dc9520e10c: failed, profile aitunnel_test, requested2000, acceptance ceiling8000, attempts10, positions0, decisions0, accepted usage0. Six received output counts2015/1865/1915/1909/1691/1823; one flagged requested-cap excess. Larger2015 was admitted by the intended output policy but rejected later by local validation. This is successful exception wiring, not a valid Position or completed live council. Four other attempts cancelled; root's bounded single diagnostic is separate and must stay unaccepted unless real guards pass.

### PI07-R01 / P2 — cancelled attempts absent from per-attempt audit

Location: council/runtime.py Council.call, record_usage and exception handlers around lines208–277. Contract PI07 requires per-attempt requested_output_tokens/exceeded with null when unknown.

Concrete actual trigger: terminal invalid sibling causes TaskGroup cancellation of pending siblings. Trace has10 registered attempts/events but only6 usage rows. Independent summary reports known outputs6/unknown outputs0, because the four unknown attempts have no rows at all. asyncio.CancelledError derives from BaseException; it bypasses both Exception handlers and record_usage. Thus the promised per-attempt audit cannot represent cancelled unknowns directly.

Effect: failure remains safely failed/no Position, but audit completeness and explicit unknown-excess accounting are lost. This is not permission to invent zero usage or consume late provider results.

Minimal fix: bounded CancelledError handler records one immutable usage row with requested cap and unknown counters/exceeded=null when unavailable, marks event cancelled/rejected, then re-raises. Preserve existing late-result discard/nonblocking cancellation; no unbounded awaiting for remote usage. Regression should cause real sibling cancellation and require a usage row for each registered event/attempt, with null unknowns and no duplicate/late accepted rows. Repeat affected/current full checks after correction before final PASS.

Reviewer performed read-only trace/code inspection, no live requests, credentials, installs, product changes or new agents. Original117 green and this actual failed audit evidence retained.

## PI07-R01 closure and final actual verdict — PASS

Actual runtime.call now explicitly catches asyncio.CancelledError, records one unknown usage row/requested cap/exceeded=null and a cancelled rejected event, then re-raises. No remote await, zero fabrication, late response admission or duplicate recording added. Existing atomic initial-five barrier/DTO/citation/unanimity safeguards remain.

Reviewer independently ran exact regression `.venv-consensus/Scripts/python.exe -m pytest council/tests/test_providers.py::test_cancelled_siblings_preserve_unknown_attempt_usage -q`: exit0,1 passed0.80s. Fixture starts all five, one terminal failure cancels four;5 events/usage rows have bijective IDs, explicitnull unknowns/requested2000, no positions/decisions. Author current full after this correction and exact-quote prompt:118 passed26.97s exit0/session45838. Historical117/cancelgap BLOCKED evidence above remains intact.

Exact-quote prompt explicitly copies punctuation/whitespace, allows JSON escaping but requires decoded contiguous substring, and forbids line joining/space normalization. Source/assumption citation requirements remain. Reviewer independently read safe b07 diagnostic: nonexact_quote with space_normalized_matches=true,2052 tokens,4 criteria/5 arguments. Specific CRLF source observation belongs to author's inspected evidence; no fuzzy citation repair or weaker guard was implemented. This prompt improves instructions without certifying compliance or semantic entailment.

Independently filtered current live f03b53115da344e7a308909e9a7ea15a trace: failed; aitunnel_test requested2000/ceiling8000;8 attempts/events/usage rows with unique bijective attempt IDs;6 received counts,2 explicitunknown rows with exceeded=null/requested2000/accepted=false. Outputs2183/2046 have excess=true and were rejected by later local checks. Two other initial responses were locally accepted, but the atomic five-position barrier did not complete: committed positions0, decisions0. There is no unanimous decision or completed live discussion. This actual trace closes the missing-cancellation-row counterexample while retaining truthful failure.

Current provider-live-verification explicitly records terminal session44982 exit1, the failed barrier, unknown cancelled costs, actual118 green and stopped blind repeats. Earlier running entries are superseded by its terminal section. The former external model/provider question is superseded by the direct conditional-test authorization, not left pending as a current dependency. Direct OpenAI live remains unrun without its own key; default strict output policies remain.

**Final independent implementation/verification verdict: PASS; observed full live protocol outcome: FAIL acknowledged.** No unresolved material product finding. PI07's planned bounded verification DoD permits an honest failure report; it cannot be relabeled no_consensus or consensus. No live reasoning-quality score, production suitability, universal accounting/remote billing guarantee or user acceptance inferred. Accepted original prototype remains preserved. Reviewer made no paid calls, credential reads, installs, product edits or new agents; only the requested focused offline regression and read-only evidence inspection.

## PI08 focused diagnostic review — original observation

User asks why a Position was not obtained. Read actual runtime.call, validate_citations, report and five new diagnostic/report regression cases. Stage is advanced only before the corresponding unchanged check: provider → response_contract → schema → citations → protocol. Accepted=true still follows all checks. Citation membership, evidence digest and exact decoded substring predicates remain mandatory; splitting their fixed exceptions does not normalize quotations or admit invalid evidence. Fixed code lookup stores no exception text. Pydantic errors retain only built-in type labels from these actual DTOs, without input/context/location/message. JSONDecodeError subclass is specifically categorized response_json without storing its doc/msg. Author current full123 passed24.62s exit0/session1908 covers this snapshot; prior122 is historical.

Report derives individual initial acceptance from events, while committed positions still require the complete five-person barrier. It correctly distinguishes a locally valid but uncommitted answer from a missing Position. Old f03 contains generic ValueError only, so its precise rejection cause cannot be reconstructed; the previous single CRLF diagnostic cannot be assigned to Robert or all of that run's failures. A new Robert diagnostic is a separate observation and must not rewrite old evidence or imply a completed council.

### PI08-R01 / P3 — cancellation cause asserted without evidence

Location: council/report.py, absent-position details branch handling last.error == CancelledError. Trigger: an initial task is cancelled directly by its owner or during external shutdown; runtime.call records CancelledError with no cause discriminator. Report nonetheless says «Запрос отменён после ошибки другого участника». Effect: correct rejected/cancelled state is given an unsupported causal explanation. Smallest fix: neutral wording such as «Запрос отменён; ответ не завершён», without adding a new cancellation-state mechanism. No evidence/consensus guard change is required. Root notified; focused disposition and final diagnostic evidence pending. Original finding preserved here.

Reviewer performs no paid calls, raw settings/credential reads, product edits, installations or new-agent work. No broad suite rerun; author123 evidence does not yet cover a future wording correction.

## PI08 final focused closure — PASS

PI08-R01/P3 closed: actual report now says «Запрос отменён; ответ не завершён», avoiding unsupported causal attribution. Existing partial-barrier regression includes a cancelled Marcus event and asserts that exact neutral wording. Author final affected check:1 passed0.93s exit0; runtime/context full123 passed24.62s exit0 remains applicable because subsequent production change is report text only. No new protocol, acceptance, retry, output-budget or quotation changes. Reviewer inspected the actual correction/fixture; no broad victory-lap rerun.

Independently read safe position-diagnosis-c9f61fa20a2f46c09142ff8efeea65b1/metadata.json and filtered trace: diagnostic_single_position, one attempt, Robert accepted=true at protocol, citation_issues empty, committed initial_positions0, decisions0, separate position.json exists. Usage is input28785/output1765/requested2000/excess=false/cost_rub0.60, returned gpt-6-luna-pro; this is the observed bounded single response, not a five-person barrier or consensus. No raw Position/source contents were needed for this closure.

Author position-diagnosis.md correctly explains historical f03: Peter/Warren individually accepted, Robert exhausted two generic ValueError attempts, pending siblings cancelled and atomic assignment never completed. The old payloads and exact ValueError causes were not retained and cannot be recovered. New Robert success is explicitly separate; it does not prove why the old response failed, prove the earlier CRLF diagnosis applies to it, or establish stochastic/semantic reliability. Original failed artifacts remain unchanged.

Final focused implementation/report-evidence verdict PASS; no unresolved material finding. User's diagnostic request is handled with the demonstrable barrier cause, explicit limit on recovering the old validation cause, improved safe logging and a separate successful live Robert observation. Previous full live council FAIL remains acknowledged. No further paid calls/full retries, credentials, product edits, installs, new agents or reopened accepted prototype gate by reviewer.
