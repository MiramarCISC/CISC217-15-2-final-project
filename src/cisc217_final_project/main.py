from pathlib import Path
from typing import Annotated
from fastapi import Depends,FastAPI,HTTPException,Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .config import GAME_CONFIG
from .database import battle_history,create_schema,get_session
from .domain import GameRuleError
from .schemas import CharacterCreate,CharacterRead,BattleResult
from .service import GameService

BASE_DIR=Path(__file__).resolve().parent; TEMPLATES_DIR=BASE_DIR/"templates"; STATIC_DIR=BASE_DIR/"static"; EXPORT_DIR=BASE_DIR/"exports"
app=FastAPI(title="CISC 217 Character Adventure Example")
app.mount("/static",StaticFiles(directory=STATIC_DIR),name="static")
templates=Jinja2Templates(directory=TEMPLATES_DIR)
SessionDep=Annotated[Session,Depends(get_session)]

@app.on_event("startup")
def startup(): create_schema()
@app.get("/")
def home(request:Request): return templates.TemplateResponse(request=request,name="index.html",context={"title":"Character Adventure"})
@app.get("/game-config")
def game_config(): return GAME_CONFIG
@app.get("/classes")
def classes(session:SessionDep): return [{"id":c.id,"name":c.name,"description":c.description} for c in GameService(session).list_classes()]
@app.get("/characters",response_model=list[CharacterRead])
def characters(session:SessionDep): return GameService(session).list_characters()
@app.post("/characters",response_model=CharacterRead,status_code=201)
def create_character(data:CharacterCreate,session:SessionDep):
    try:return GameService(session).create_character(data)
    except GameRuleError as e: raise HTTPException(status_code=400,detail=str(e)) from e
@app.delete("/characters/{character_id}")
def delete_character(character_id:int,session:SessionDep):
    if not GameService(session).delete_character(character_id): raise HTTPException(status_code=404,detail="Character not found")
    return {"deleted":True}
@app.post("/characters/{character_id}/battle/{enemy_name}",response_model=BattleResult)
def battle(character_id:int,enemy_name:str,session:SessionDep):
    try:return GameService(session).battle(character_id,enemy_name)
    except GameRuleError as e: raise HTTPException(status_code=400,detail=str(e)) from e
@app.get("/party-summary")
def summary(session:SessionDep): return GameService(session).party_summary()
@app.get("/battle-history")
def history(): return battle_history()
@app.get("/export/json")
def export_json(session:SessionDep):
    p=GameService(session).export_json(EXPORT_DIR); return FileResponse(p,media_type="application/json",filename=p.name)
@app.get("/export/csv")
def export_csv(session:SessionDep):
    p=GameService(session).export_csv(EXPORT_DIR); return FileResponse(p,media_type="text/csv",filename=p.name)
