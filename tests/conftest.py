import sqlite3,tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker
import cisc217_final_project.database as database
from cisc217_final_project.database import get_session
from cisc217_final_project.main import app
from cisc217_final_project.models import Base

@pytest.fixture
def env(monkeypatch):
    with tempfile.TemporaryDirectory() as td:
        db=Path(td)/"test.db"; eng=create_engine(f"sqlite:///{db}",connect_args={"check_same_thread":False}); Base.metadata.create_all(eng)
        with sqlite3.connect(db) as c:c.execute("CREATE TABLE battle_log (id INTEGER PRIMARY KEY AUTOINCREMENT, character_id INTEGER NOT NULL, enemy_name TEXT NOT NULL, damage INTEGER NOT NULL, experience_gained INTEGER NOT NULL)");c.commit()
        factory=sessionmaker(bind=eng,class_=Session,expire_on_commit=False); monkeypatch.setattr(database,"DATABASE_PATH",db)
        def override():
            with factory() as s: yield s
        app.dependency_overrides[get_session]=override; yield factory; app.dependency_overrides.clear();eng.dispose()
@pytest.fixture
def client(env):
    with TestClient(app) as c: yield c
