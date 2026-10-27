# Research checkpoint: beyond ETH

Дата: 27 октября 2026. Самодостаточный результат текущего исследовательского сеанса.

Начать с [research_checkpoint_ru.md](research_checkpoint_ru.md). В нём:

- условный RP-SUBEXP алгоритм для sparse SCGS через ordinary #3SAT и линейную изоляцию;
- новые для текущей программы алгоритмические следствия, точный учёт параметров и полные доказательства;
- input-preserving BP-to-graphic/cographic-span reduction;
- доказательство `deterministic LGS SUBEXP => NEXP not subseteq L/poly`;
- условный запрет слишком коротких polynomial-time reverse reductions через SAT compression;
- три конкретных следующих направления.

Полная win-win с lower bounds для большого семейства классических задач и `NEXP not subseteq P/poly` **не установлена**. Утверждения, использующие октябрьскую #SAT-теорему, явно условны; её независимая проверка здесь не выполнена. Randomized и deterministic утверждения разделены.

## Приложения

- `sat_status.md`: проверенные первичные источники и дополнительный exact-counting аргумент.
- `parity_rank.md`: расширенные rank/parity proofs, альтернативная изоляция и дальнейшие weighted вопросы.
- `williams.md`: circuit transfer, direct BP gadget, барьеры и полные доказательства.
- `verify_checkpoint.py`: независимые конечные проверки, только стандартная библиотека Python 3.10+.
- `verification.json`: результат запуска; внешний SAT/hash/Williams theorem не проверяется этим скриптом.

Запуск: `python verify_checkpoint.py`. Скрипт обновляет только соседний `verification.json`.

Для GitHub все файлы добавляются в `research/6.1-winwin/` на одноимённой отдельной ветке. База: `4889bc8ccadd140bcb022866e9cf048b33e4accf`. Существующие исследовательские ветки и `main` не изменяются.
