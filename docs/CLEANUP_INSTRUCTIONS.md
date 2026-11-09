# Required cleanup before starting your own final project

This repository begins with a fully working **Character Adventure** example based on the earlier character labs.

You may inspect and run it, but do not submit it as your final project.

## Run the example

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
uvicorn cisc217_final_project.main:app --reload
```

## Test the working example

One temporary cleanup-guard test intentionally fails while the instructor code remains. Run the example tests with:

```bash
python -m pytest -q -k "not instructor_example_has_been_removed"
```

## Remove the provided solution

Before starting your project:

```bash
python scripts/cleanup_example.py
```

The script replaces the instructor source with the minimal scaffold and deletes all provided example tests, including the temporary cleanup guard.

Then create your own tests in `tests/` and implement your own application.
