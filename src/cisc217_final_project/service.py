import csv,json
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from .config import GAME_CONFIG
from .database import record_battle
from .domain import CombatRules,GameRuleError,Party
from .models import Character,CharacterClass
from .schemas import CharacterCreate,BattleResult

class GameService:
    def __init__(self,session:Session): self.session=session; self.rules=CombatRules()
    def ensure_default_classes(self):
        if self.session.scalar(select(CharacterClass.id).limit(1)) is not None: return
        self.session.add_all([CharacterClass(name="Warrior",description="High health"),CharacterClass(name="Mage",description="High power"),CharacterClass(name="Rogue",description="Balanced")]); self.session.commit()
    def list_classes(self): self.ensure_default_classes(); return list(self.session.scalars(select(CharacterClass).order_by(CharacterClass.id)).all())
    def list_characters(self): return list(self.session.scalars(select(Character).order_by(Character.id)).all())
    def create_character(self,data:CharacterCreate):
        self.ensure_default_classes()
        if self.session.get(CharacterClass,data.class_id) is None: raise GameRuleError("character class not found")
        c=Character(name=data.name.strip(),class_id=data.class_id,health=data.health,power=data.power); self.session.add(c); self.session.commit(); self.session.refresh(c); return c
    def delete_character(self,character_id:int):
        c=self.session.get(Character,character_id)
        if c is None:return False
        self.session.delete(c); self.session.commit(); return True
    def battle(self,character_id:int,enemy_name:str):
        c=self.session.get(Character,character_id)
        if c is None: raise GameRuleError("character not found")
        enemies=GAME_CONFIG["enemies"]
        if enemy_name not in enemies: raise GameRuleError("enemy not found")
        enemy=enemies[enemy_name]; damage=self.rules.calculate_damage(c.power,int(enemy["defense"])); xp=int(enemy["experience"]); c.experience+=xp
        leveling=GAME_CONFIG["leveling"]; threshold=int(leveling["experience_per_level"]); leveled=False
        while c.experience>=c.level*threshold:
            c.level+=1; c.health+=int(leveling["health_gain"]); c.power+=int(leveling["power_gain"]); leveled=True
        self.session.commit(); self.session.refresh(c); record_battle(c.id,enemy_name,damage,xp)
        return BattleResult(attacker=c.name,enemy=enemy_name,damage=damage,experience_gained=xp,leveled_up=leveled,new_level=c.level,new_experience=c.experience)
    def party_summary(self):
        p=Party(self.list_characters()); strongest=p.strongest
        return {"count":len(p),"total_power":p.total_power,"strongest":strongest.name if strongest else None,"top_characters":[c.name for c in p.top(3)]}
    def export_json(self,d:Path):
        d.mkdir(parents=True,exist_ok=True); out=d/"characters.json"; out.write_text(json.dumps([{k:getattr(c,k) for k in ("id","name","level","health","power","experience","class_id")} for c in self.list_characters()],indent=2)); return out
    def export_csv(self,d:Path):
        d.mkdir(parents=True,exist_ok=True); out=d/"characters.csv"; fields=["id","name","level","health","power","experience","class_id"]
        with out.open("w",newline="") as h:
            wr=csv.DictWriter(h,fieldnames=fields); wr.writeheader(); [wr.writerow({k:getattr(c,k) for k in fields}) for c in self.list_characters()]
        return out
