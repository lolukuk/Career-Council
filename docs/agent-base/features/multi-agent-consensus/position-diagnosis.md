# Почему в последнем полном запуске нет позиций

2026-10-09. Проверка по прямому запросу пользователя. Исходный артефакт: `council/output/f03b53115da344e7a308909e9a7ea15a/trace.json`, оригинал не изменён.

Подтверждено по событиям: Peter Thiel и Warren Buffett дали ответы, принятые индивидуальным валидатором с первой попытки. Robert Reich дважды получил ValueError; повторные запросы Nassim Nicholas Taleb и Marcus Aurelius отменены после исчерпания его двух попыток. Анализ всех пяти не завершён. `Council.analyze` присваивает `self.positions` только после успешного полного barrier. Поэтому в trace нет зафиксированных initial_positions и нет проекта решения, несмотря на два ранее принятых индивидуальных ответа. Их тексты старый trace не сохранил; восстановление не заявляется.

Старый отчёт «Позиция не получена» недостаточно точно описывал этот случай. Report теперь отличает принятый индивидуальный ответ от незафиксированного общего этапа. Отмена подписана нейтрально: сама по себе не доказывает причину отмены.

Точное условие старых ValueError определить по исходному trace нельзя: сохранён только тип исключения, без этапа/кода проверки и без payload. Не приписываем им автоматически неточную цитату или превышение токенов. Отдельная прежняя диагностика b07 установила склейку CRLF в цитате, но не является доказательством причины именно старых ответов Reich.

Исправление диагностики: safe validation_stage и whitelist validation_code в attempt events; отдельно различаются неточная цитата, непоказанный chunk, несовпадение digest, структура DTO, IDs и некоторые provider-envelope/usage ошибки. Pydantic сохраняет только встроенные типы ошибок, без input/context/location/message. Raw exception text, provider error body и отвергнутые raw outputs не пишутся. Исходные проверяемые условия и поведение retries/barrier/consensus не изменены, нормализации цитат нет.

Свежая ограниченная проверка только Reich: `Council.call`, max2 frozen attempts,45s, AI Tunnel gpt-6-luna-pro/none/explicit test mode, реальное досье и настоящие schema/citation/unique-ID guards. **exit0/PASS с первой попытки**, input28785/output1765, reported cost0.60rubles. Артефакты: `council/output/position-diagnosis-c9f61fa20a2f46c09142ff8efeea65b1/{report.md,metadata.json,position.json,trace.json}`. Статус diagnostic_single_position, не пятисторонний run/решение/консенсус. Новый успешный ответ не восстанавливает неизвестную причину старого неуспеха.

Full applicable check после диагностических runtime/context изменений: `.venv-consensus/Scripts/python.exe -m pytest council/tests -q` → **123 passed24.62s, exit0**. После этого независимый reviewer выявил небольшую P3 неточность подписи отмены; root исправил только подпись и расширил существующий report regression. Focused check для окончательной подписи и independent closure фиксируются ниже. Исторический122/30.03 predates JSONDecodeError category fix; не объявляется текущей финальной проверкой.

Focused final report-copy regression:1 passed0.93s, exit0. Independent final closure pending.


PI08 finalclosure2026-10-09: existing reviewer actualfocusedPASS recordedhandoffs/provider-review/live-result.md/todo.md; PI08-R01/P3closed. Independently inspected newRobert safe metadata/trace verifiesonevalidinitial/0fullbarrier/0decisions; originalf03precisecauseunknown andfailedhistory retained. Authorruntime/context full123/24.62exit0 +copy-onlyaffected1/0.93exit0, no remainingmaterialcorrections. Requesteddiagnosis andsafejournal/reportfix complete; no liveconsensus/productionclaim.
