# PI06 actual independent review

2026-10-09. Reviewer: consensus_design_review, author: root. Approved B reviewed against actual settings/providers/model/runtime/main/report/README, provider fixtures and current verification. Accepted original prototype15 preserved.

## Initial verdict: BLOCKED pending PI-R01 correction

Author evidence: full ` .venv-consensus/Scripts/python.exe -m pytest council/tests -q` exit0,95 passed25.79s. This does not cover the two independently reproduced cases below. A subsequent test-only credential-isolation correction needs current full rerun. No actual provider connectivity/quality claim.

### PI-R01 / P2 — HTTP200 transient error classified terminal

Location: council/providers.py `_http`, lines190–191; approved contracts "429/5xx/network timeout — bounded retry".

Trigger: MockTransport returns HTTP200 envelope `error.code=429`, with valid reported usage. Same issue for provider error502/503 carried inside200, which AIT documents for failures after generation.

Effect: invoke raises terminal ProviderRequestError, so Council does not apply the prescribed bounded transient retry. The safe envelope check prevents invalid consensus, but turns recoverable provider failure into failed run.

Independent offline result: `HTTP200/code429: ProviderRequestError usage=2`, exit0. No real HTTP or key use.

Smallest fix: classify numeric body error.code using explicit auth/transient/terminal categories; unknown code stays terminal. Keep usage capture before rejection, no raw message/metadata logging. Add HTTP200 error429/503 retry and400/401 terminal fixtures, same frozen input/max2 constraints.

### PI-R02 / P3 — completed expired inner task exception unconsumed

Location: council/model.py `invoke`, finally lines136–141. Historical cleanup reasoning R15 remains applicable inside the new perform task; Council consumes only its outer invoke task.

Trigger: generate finishes by raising after the absolute attempt expiry, before invoke resumes. Independent bounded scripted reproduction used synchronous10ms completion followed by RuntimeError, timeout1ms.

Effect: invoke raises TimeoutError without retrieving completed perform-task exception; loop emits `Task exception was never retrieved`. Late output is denied correctly, but cleanup diagnostics can escape the intended boundary.

Independent result: loop handler captured exactly `["Task exception was never retrieved"]`, exit0.

Smallest fix: finally call discard_task(task) when already done, retaining callback on pending tasks. Add inner-task completed-expiry fixture with loop warning capture; not only Council outer-task fixture.

## Other actual checks

Read-only evidence confirms policy distinction/reliable=false AIT, preparation catalog before disclosure, provider-specific key selection/no legacy fallback, frozen count/generation input/schema, wire/output caps, transport-default/tuple normalization followed by original DTO/citation validation, refusal/model mismatch rejection, captured usage for rejected200 responses, closed audit preventing late preflight generation, fixed endpoints/no redirects/proxy routing, bounded client close and truthful reports. Reviewed fixtures cover both adapters and agree/revise/disagree without claiming live reasoning.

OpenAI32768 remains an application token budget; exact count is not certification of every user's model window. AIT remote context enforcement/internal retries/backend revision/billing after cancellation remain documentary limitations. No new architecture/provider restriction is required for either finding.

Current reviewer activity: code/document inspection plus one short offline MockTransport/scripted reproduction, no raw.env/credentials/live requests/install/product edits/new agents. Await author fixes, focused regression and current full check before final closure.

## Final closure — PASS / 2026-10-09

**Current PI06 verdict: PASS. PI-R01 and PI-R02 closed.** Initial BLOCKED verdict, original counterexamples and95-test evidence above remain historical. Author supplied current full result: `.venv-consensus/Scripts/python.exe -m pytest council/tests -q` → exit0, **103 passed24.19s**, session4121. Reviewer did not repeat that broad suite; independently inspected actual correction and repeated both original short offline reproductions. No subsequent production edits reported.

- PI-R01: `_http` now classifies numeric/three-digit string body codes401/403 as auth,429/5xx as transient, other/unknown as terminal. Usage capture remains before error handling. Same independent HTTP200/code429 reproduction now produced `TransientModelError usage=2`, exit0. Actual runtime fixtures cover status and200-body401/429/400/503, correct1/2-attempt maxima, retained rejected usage and safe category trace.
- PI-R02: invoke finally now retrieves already-done inner-task exception, retaining pending cancellation callback. Same expired completed-task reproduction now produced warning list `[]`, exit0. Added `test_already_done_expired_inner_error_is_consumed` captures loop warnings after expiry, GC and event-loop resumption.
- Current test isolation excludes personal.env/environment from unconfigured CLI checks. Positive mock CLI lifecycle tests for both providers use only synthetic credentials, save consensus trace/report and assert HTTP client closed. These exercise CLI/adapters/resources with fixture reasoning; they do not demonstrate live model quality.

PASS covers actual approved provider integration and local protocol boundary evidence. It does not certify arbitrary model compatibility, remote context enforcement/backend revision, provider connectivity, reasoning quality or remote cancellation/cost. No raw.env/keys/live calls/installs/product edits/new agents by reviewer. Original accepted prototype15 remains accepted; successor user acceptance is separate and not declared here. Root should record103 as current evidence in author verification/status, preserving95 as history.
