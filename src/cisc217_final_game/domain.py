from collections.abc import Iterator
from .models import Character

class GameRuleError(ValueError):
    pass

class CombatRules:
    def calculate_damage(self,power:int,defense:int)->int:
        if power < 1: raise GameRuleError("power must be positive")
        if defense < 0: raise GameRuleError("defense cannot be negative")
        return max(1,power-defense)

class Party:
    def __init__(self,characters:list[Character],rules:CombatRules|None=None):
        self._characters=list(characters)
        self._rules=rules or CombatRules()
    def __iter__(self)->Iterator[Character]: return iter(self._characters)
    def __len__(self)->int: return len(self._characters)
    def __contains__(self,name:object)->bool: return any(c.name==name for c in self._characters)
    @property
    def total_power(self)->int: return sum(c.power for c in self._characters)
    @property
    def strongest(self)->Character|None: return max(self._characters,key=lambda c:c.power,default=None)
    def ranked(self)->list[Character]: return sorted(self._characters,key=lambda c:(-c.level,-c.power,c.name.lower()))
    def top(self,limit:int=3)->list[Character]: return self.ranked()[:limit]
    def experienced(self,minimum:int)->Iterator[Character]:
        for c in self._characters:
            if c.experience>=minimum: yield c
