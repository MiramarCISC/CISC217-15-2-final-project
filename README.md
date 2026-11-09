# CISC 217 Final Project — Character Adventure Example

This Classroom50 repository starts with a fully working **Character Adventure** example that extends the character-management labs from the course.

It demonstrates one coherent way to integrate all 15 required topics.

**Do not submit the provided implementation.**

Before starting your own project, run:

```bash
python scripts/cleanup_example.py
```

See:

```text
docs/CLEANUP_INSTRUCTIONS.md
```

## Example Workflow

Create a character → persist it with SQLAlchemy/SQLite → fight enemies → gain XP and level up → view party summaries and battle history → export character data as JSON/CSV.

## Create the Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
```

## One-Time JupyterHub Proxy Setup

The FastAPI web application runs inside your JupyterHub container. To open it in your browser, JupyterHub must proxy the application's local port.

Check whether `jupyter-server-proxy` is already available in the Python environment that runs JupyterHub:

```bash
/opt/conda/bin/python -m pip show jupyter-server-proxy
```

If it is not installed, install it into your JupyterHub user environment:

```bash
/opt/conda/bin/python -m pip install --user jupyter-server-proxy
```

Enable the extension:

```bash
/opt/conda/bin/jupyter server extension enable \
  --py jupyter_server_proxy \
  --user
```

Verify that it is enabled:

```bash
/opt/conda/bin/jupyter server extension list | grep -i -A3 proxy
```

You should see output similar to:

```text
jupyter_server_proxy enabled
- Validating jupyter_server_proxy...
  jupyter_server_proxy ... OK
```

### Restart JupyterHub After Enabling the Proxy

If you just installed or enabled `jupyter-server-proxy`, restart your JupyterHub server/session so the running Jupyter server loads the extension.

After reconnecting, open a terminal and verify again:

```bash
/opt/conda/bin/jupyter server extension list | grep -i -A3 proxy
```

## Run the Example in JupyterHub

Activate the project virtual environment:

```bash
source .venv/bin/activate
```

Start FastAPI with the JupyterHub proxy path:

```bash
uvicorn cisc217_final_project.main:app \
  --host 127.0.0.1 \
  --port 8000 \
  --root-path "${JUPYTERHUB_SERVICE_PREFIX}proxy/8000"
```

Leave this terminal running.

Open the application using:

```text
https://sdccd-jupyterhub.nrp-nautilus.io/hub/user-redirect/proxy/8000
```

The redirect automatically sends you to your own JupyterHub server.

You can also print your JupyterHub service prefix with:

```bash
echo "$JUPYTERHUB_SERVICE_PREFIX"
```

For example:

```text
/user/yourname@sdccd.edu/
```

The proxied application path is then:

```text
/user/yourname@sdccd.edu/proxy/8000
```

## Verify FastAPI Directly

If the browser page does not load, first verify that FastAPI itself is running:

```bash
curl -i http://127.0.0.1:8000/
```

You should receive:

```text
HTTP/1.1 200 OK
```

If this works but the browser proxy URL does not, check the JupyterHub proxy configuration rather than changing your FastAPI application.

## JupyterHub Proxy-Aware Web Applications

The starter project is configured so static files and JavaScript API requests work through the JupyterHub proxy.

The application uses FastAPI's `root_path` when generating URLs for:

- CSS;
- JavaScript;
- API requests;
- JSON exports;
- CSV exports.

Your browser code should not assume that the application always runs directly at `/`.

For example, JavaScript API requests should use the application root:

```javascript
const APP_ROOT = window.APP_ROOT || "";

fetch(`${APP_ROOT}/characters`);
```

instead of:

```javascript
fetch("/characters");
```

This allows the same application to work both locally and behind the JupyterHub proxy.

## Run Locally Outside JupyterHub

If you are running the project directly on your own computer rather than through JupyterHub, you can use:

```bash
uvicorn cisc217_final_project.main:app \
  --reload \
  --host 127.0.0.1 \
  --port 8000
```

Then open:

```text
http://127.0.0.1:8000/
```

## Verify the Instructor Example

The repository initially contains a temporary cleanup test that intentionally fails while the instructor example remains.

To verify only the provided example:

```bash
python -m pytest -q \
  -k "not instructor_example_has_been_removed"
```

## Remove the Instructor Example

Before beginning your own final project, run:

```bash
python scripts/cleanup_example.py
```

The cleanup script removes the provided example implementation and temporary instructor tests and leaves you with a minimal project scaffold.

After cleanup:

```bash
git status
```

Then begin implementing your own application and tests.

## Example Evidence Map

| # | Topic | Example Integration |
|---|---|---|
| 1 | Lists, tuples, sorting, slicing | `Party.ranked()` and `Party.top()` rank and slice the party. |
| 2 | Dictionaries/nested collections | `GAME_CONFIG` stores enemies and leveling rules used by battles. |
| 3 | Text/CSV/JSON/API formats | FastAPI JSON plus CSV/JSON character exports. |
| 4 | Paths/OS/persistence | `pathlib` builds data/export paths; SQLite persists characters. |
| 5 | Exceptions/validation | Pydantic plus `GameRuleError`. |
| 6 | Modules/public APIs | Models, schemas, domain, service, database, API, and UI are separated. |
| 7 | Unit testing | pytest covers domain, API, battle, export, and UI behavior. |
| 8 | Classes/composition | `Party` composes `CombatRules`; the service composes game behavior. |
| 9 | Encapsulation/properties | `_characters`, `total_power`, and `strongest`. |
| 10 | Iterators/generators/protocols | `__iter__`, `__len__`, `__contains__`, and `experienced()`. |
| 11 | Basic SQL/SQLite | Parameterized battle-log `INSERT` and `SELECT`. |
| 12 | SQLAlchemy ORM | Character/Class models, relationships, sessions, CRUD, and leveling persistence. |
| 13 | Web API behavior | Character, class, battle, summary, history, and export endpoints. |
| 14 | Web UI behavior | Jinja2 + JavaScript create characters, start battles, and refresh the UI. |
| 15 | Full integration | Browser → FastAPI → validation/rules → ORM/SQLite → response → UI. |

## Final Project Reminder

Your final project must replace the instructor example with your own application.

All 15 required course topics must:

- be meaningfully integrated into the main application;
- be reachable through the normal application workflow;
- have at least one relevant passing unit test;
- be documented in `README.md`;
- identify source-file and line-number evidence;
- identify relevant test evidence.

Your complete test suite should run with:

```bash
python -m pytest -q
```

Your finished project must run successfully in NRP JupyterHub.