import sqlite3
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from .models import Base

BASE_DIR=Path(__file__).resolve().parent
DATA_DIR=BASE_DIR/"data"; DATA_DIR.mkdir(exist_ok=True)
DATABASE_PATH=DATA_DIR/"game.db"
engine=create_engine(f"sqlite:///{DATABASE_PATH}",connect_args={"check_same_thread":False})
SessionLocal=sessionmaker(bind=engine,class_=Session,expire_on_commit=False)

def create_schema():
    Base.metadata.create_all(engine)
    with sqlite3.connect(DATABASE_PATH) as c:
        c.execute("CREATE TABLE IF NOT EXISTS battle_log (id INTEGER PRIMARY KEY AUTOINCREMENT, character_id INTEGER NOT NULL, enemy_name TEXT NOT NULL, damage INTEGER NOT NULL, experience_gained INTEGER NOT NULL)")
        c.commit()

def get_session():
    with SessionLocal() as s: yield s

def record_battle(character_id:int,enemy_name:str,damage:int,xp:int):
    with sqlite3.connect(DATABASE_PATH) as c:
        c.execute("INSERT INTO battle_log(character_id,enemy_name,damage,experience_gained) VALUES (?,?,?,?)",(character_id,enemy_name,damage,xp)); c.commit()

def battle_history(limit:int=10):
    with sqlite3.connect(DATABASE_PATH) as c:
        c.row_factory=sqlite3.Row
        rows=c.execute("SELECT id,character_id,enemy_name,damage,experience_gained FROM battle_log ORDER BY id DESC LIMIT ?",(limit,)).fetchall()
    return [dict(r) for r in rows]
