from pydantic import BaseModel, ConfigDict, Field

class CharacterCreate(BaseModel):
    name: str = Field(min_length=1,max_length=40)
    class_id: int
    health: int = Field(default=100,ge=1,le=200)
    power: int = Field(default=10,ge=1,le=100)

class CharacterRead(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; name:str; level:int; health:int; power:int; experience:int; class_id:int

class BattleResult(BaseModel):
    attacker:str; enemy:str; damage:int; experience_gained:int; leveled_up:bool; new_level:int; new_experience:int
