import json
from pathlib import Path
from cisc217_final_game.service import GameService
from cisc217_final_game.schemas import CharacterCreate

def test_exports(env,tmp_path):
    factory=env
    with factory() as s:
        svc=GameService(s); svc.create_character(CharacterCreate(name="Cyra",class_id=1,health=90,power=25)); jp=svc.export_json(tmp_path); cp=svc.export_csv(tmp_path)
    assert json.loads(jp.read_text())[0]["name"]=="Cyra"; assert "Cyra" in cp.read_text()
