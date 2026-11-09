# CISC 217 Final Project — Character Adventure Example

This Classroom50 repository starts with a fully working **Character Adventure** example that extends the character-management labs from the course.

It demonstrates one coherent way to integrate all 15 required topics. **Do not submit the provided implementation.** Before starting your own project, run:

```bash
python scripts/cleanup_example.py
```

See `docs/CLEANUP_INSTRUCTIONS.md`.

## Example workflow

Create a character → persist it with SQLAlchemy/SQLite → fight enemies → gain XP and level up → view party summaries and battle history → export character data as JSON/CSV.

## Run the example

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
uvicorn cisc217_final_project.main:app --reload
```

## Verify the instructor example

```bash
python -m pytest -q -k "not instructor_example_has_been_removed"
```

## Example evidence map

| # | Topic | Example integration |
|---|---|---|
| 1 | Lists, tuples, sorting, slicing | `Party.ranked()` and `Party.top()` rank and slice the party. |
| 2 | Dictionaries/nested collections | `GAME_CONFIG` stores enemies and leveling rules used by battles. |
| 3 | Text/CSV/JSON/API formats | FastAPI JSON plus CSV/JSON character exports. |
| 4 | Paths/OS/persistence | `pathlib` builds data/export paths; SQLite persists characters. |
| 5 | Exceptions/validation | Pydantic plus `GameRuleError`. |
| 6 | Modules/public APIs | Models, schemas, domain, service, database, API, UI separated. |
| 7 | Unit testing | pytest covers domain, API, battle, export, and UI behavior. |
| 8 | Classes/composition | `Party` composes `CombatRules`; service composes game behavior. |
| 9 | Encapsulation/properties | `_characters`, `total_power`, and `strongest`. |
| 10 | Iterators/generators/protocols | `__iter__`, `__len__`, `__contains__`, `experienced()`. |
| 11 | Basic SQL/SQLite | Parameterized battle-log INSERT and SELECT. |
| 12 | SQLAlchemy ORM | Character/Class models, relationships, sessions, CRUD, leveling persistence. |
| 13 | Web API behavior | Character/class/battle/summary/history/export endpoints. |
| 14 | Web UI behavior | Jinja2 + JavaScript create characters, start battles, refresh UI. |
| 15 | Full integration | Browser → FastAPI → validation/rules → ORM/SQLite → response → UI. |
