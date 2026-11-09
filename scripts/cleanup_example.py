"""Remove the instructor example and create the student final-project scaffold."""

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "src" / "cisc217_final_project"
TESTS_DIR = ROOT / "tests"


SCAFFOLDS = {
    PKG / "models.py": '''"""Define your SQLAlchemy ORM models here."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for your ORM models."""


# TODO: Define your project's persistent domain models.
''',

    PKG / "schemas.py": '''"""Define your Pydantic API schemas here."""

from pydantic import BaseModel


# TODO: Define request and response schemas for your project.
''',

    PKG / "database.py": '''"""Configure persistence for your final project."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "app.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)


def create_schema() -> None:
    """Create all SQLAlchemy ORM tables."""
    Base.metadata.create_all(engine)


def get_session():
    """Provide one SQLAlchemy session to FastAPI."""
    with SessionLocal() as session:
        yield session


# TODO:
# Add meaningful direct SQLite operations if your Topic 11
# implementation requires them.
''',

    PKG / "domain.py": '''"""Domain objects and Python behavior for your final project."""

# TODO:
# Integrate classes/composition, encapsulation/properties,
# iterators/generators/protocols, exceptions, and validation
# into your application's normal workflow.
''',

    PKG / "config.py": '''"""Structured application configuration."""

APP_CONFIG = {}

# TODO:
# Add meaningful dictionaries or nested collections used
# by the actual application.
''',

    PKG / "service.py": '''"""Application/service layer."""

# TODO:
# Implement reusable application logic here.
''',

    PKG / "main.py": '''"""FastAPI application for your CISC 217 final project."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import create_schema


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="CISC 217 Final Project")

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)

templates = Jinja2Templates(
    directory=TEMPLATES_DIR
)


@app.on_event("startup")
def startup() -> None:
    """Create the database schema."""
    create_schema()


@app.get("/")
def home(request: Request):
    """Render the main application page."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "CISC 217 Final Project",
        },
    )


# TODO:
# Add your project's API routes and integrated behavior.
''',

    PKG / "templates" / "index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>{{ title }}</title>

    <link
        rel="stylesheet"
        href="{{ url_for('static', path='/styles.css') }}"
    >
</head>
<body>
    <main class="container">
        <h1>{{ title }}</h1>

        <p>
            Replace this scaffold with your own
            integrated application user interface.
        </p>

        <!-- TODO: Build your project UI. -->
    </main>

    <script
        src="{{ url_for('static', path='/app.js') }}"
    ></script>
</body>
</html>
''',

    PKG / "static" / "styles.css": '''body {
    font-family: Arial, sans-serif;
    margin: 0;
}

.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 1rem;
}

/* TODO: Add your project styles. */
''',

    PKG / "static" / "app.js": '''"use strict";

// TODO:
// Add browser behavior and API integration
// for your final project.
''',
}


def replace_example_source() -> None:
    """Replace instructor implementation with student scaffolds."""
    for path, content in SCAFFOLDS.items():
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        path.write_text(content)


def remove_example_tests() -> None:
    """Remove instructor-provided tests."""
    if not TESTS_DIR.exists():
        return

    for test_file in TESTS_DIR.glob("test_*.py"):
        test_file.unlink()

    conftest = TESTS_DIR / "conftest.py"

    conftest.write_text(
        '"""Shared pytest fixtures for your final project."""\n\n'
        "# TODO: Add fixtures for your project.\n"
    )


def remove_generated_files() -> None:
    """Remove runtime files generated by the example."""

    data_dir = PKG / "data"

    if data_dir.exists():
        for pattern in (
            "*.db",
            "*.sqlite",
            "*.sqlite3",
        ):
            for database_file in data_dir.glob(pattern):
                database_file.unlink()

    exports_dir = PKG / "exports"

    if exports_dir.exists():
        shutil.rmtree(exports_dir)

    for cache_dir in ROOT.rglob("__pycache__"):
        shutil.rmtree(
            cache_dir,
            ignore_errors=True,
        )


def remove_example_marker() -> None:
    """Remove the marker used by the temporary cleanup test."""
    marker = (
        ROOT
        / "PROVIDED_EXAMPLE_CODE_PRESENT.txt"
    )

    if marker.exists():
        marker.unlink()


def main() -> None:
    """Convert the instructor example into the student scaffold."""

    if not PKG.exists():
        raise SystemExit(
            f"Expected package directory not found: {PKG}"
        )

    replace_example_source()
    remove_example_tests()
    remove_generated_files()
    remove_example_marker()

    print(
        "Instructor Character Adventure example removed."
    )
    print(
        "Student final-project scaffold created."
    )
    print(
        "Create your own tests under tests/."
    )


if __name__ == "__main__":
    main()