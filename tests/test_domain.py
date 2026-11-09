from cisc217_final_game.domain import Party,CombatRules
from cisc217_final_game.models import Character

def test_domain_protocols():
    chars=[Character(id=1,name="Aria",class_id=1,level=2,health=100,power=20,experience=60),Character(id=2,name="Borin",class_id=1,level=1,health=100,power=15,experience=20)]
    p=Party(chars); assert len(p)==2; assert "Aria" in p; assert p.total_power==35; assert p.strongest.name=="Aria"; assert [c.name for c in p.top(1)]==["Aria"]; assert [c.name for c in p.experienced(50)]==["Aria"]; assert CombatRules().calculate_damage(10,3)==7
