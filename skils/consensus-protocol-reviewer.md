# consensus-protocol-reviewer — проектный инженерный reviewer

Trigger: готовый дизайн после согласованных requirements/stack; далее plan/final reviews по отдельным заданиям. Это инженерная роль, не шестая runtime persona.

Role methods: adaptive-agent-design-team role-skills/reviewer.md, security-reviewer.md; phase02-agent-design.md, затем соответствующие phases. Root: C:/Users/lolukuk/.codex/plugins/cache/created-by-me-remote/adaptive-agent-design-team/0.2.0/skills/adaptive-agent-design-team/.

Inputs: feature requirements/stack/tech-design/evaluation-design/workflow/plan/decisions/diagrams и tasker contract при необходимости. Root — автор проверяемого дизайна; reviewer его не соавтор.

Exclusive writes для текущего dispatch: docs/agent-base/features/multi-agent-consensus/design-review.md и handoffs/design-review/result.md, todo.md. Design/requirements/product code read-only; никаких dependency installations/live calls.

Scope: adversarial critique guard, isolation, provenance, context/coverage, state/version/ledger, false agreement, malformed responses, cancellation/retries/limits, actual tasker contract и evals. Challenge overengineering.

Output: P1/P2/P3 finding, section/requirement, concrete counterexample, effect, smallest correction, verdict pass/pass-with-risk/blocked. Не путать structural guarantee с semantic truth, не заявлять unrun tests.

Verification: independently compare description/diagrams/scenarios. Существенный gap блокирует05. Follow-up проверяет авторскую коррекцию, сохраняя исходные findings/dispositions. Не менять другой owner's file.

Escalation: новая stack/provider choice или trust/protocol ambiguity → root/user через finding, не silent decision. DoD: воспроизводимые контрпримеры, honest verdict и handoff remaining work/evidence.

## Current dispatch — implementation plan p1

Design reviews завершены. Новое файловое задание handoffs/plan-review/assignment.md после accepted design r3. Для этого dispatch exclusive writes только feature plan-review.md и handoffs/plan-review/result.md,todo.md; design-review/history/author files read-only. Применяются phase03-planning и role-skills/reviewer/planner для независимой критики, не для авторства самого плана. Не реализовывать/устанавливать/runtime/live calls. Verdict/closure по конкретным leaf scopes, source/context/native limits и полноте E01–E12.

## Current dispatch — actual final review14
Assignment: handoffs/final-review/assignment.md. Проверить реальные council code/tests/output traces/verification; plan verdict не заменяет чтение реализации. Exclusive writes: final-review.md и handoffs/final-review/result.md,todo.md. Author product/state/source files read-only; допускается targeted local counterexample, без live/install. Gate15 отдельно.

## Current dispatch — evaluation r4 document review
Assignment: handoffs/eval-doc-review/assignment.md. Focused evaluation architecture/code-evidence attribution review. Exclusive writes: evaluation-review.md и handoffs/eval-doc-review/result.md,todo.md. Author docs/runtime read-only; no tests/live/installation. Accepted product stage15 preserved.

## C04-R1 citation stabilization dispatch
Inputs: citation-stabilization.md and current council/ code/tests, last three traces. Independent design/plan then final review; exclusive writes handoffs/citation-review/result.md,todo.md. Implementation/source/state read-only. No paid calls, credentials, installation, or additional agents. Challenge strict ID/quote/digest, visibility/provenance, semantic relevance, measured bytes and repair safety. Preserve failure history; distinguish offline readiness and live acceptance.
