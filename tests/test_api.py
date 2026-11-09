def test_full_flow(client):
    classes=client.get("/classes"); assert classes.status_code==200
    created=client.post("/characters",json={"name":"Aria","class_id":1,"health":100,"power":20}); assert created.status_code==201; c=created.json()
    assert client.get("/characters").json()[0]["name"]=="Aria"
    battle=client.post(f"/characters/{c['id']}/battle/Dragon"); assert battle.status_code==200; assert battle.json()["new_level"]==2
    assert client.get("/party-summary").json()["count"]==1
    assert client.get("/battle-history").json()[0]["enemy_name"]=="Dragon"

def test_validation(client):
    client.get("/classes")
    assert client.post("/characters",json={"name":"X","class_id":999,"health":100,"power":10}).status_code==400
    cfg=client.get("/game-config").json(); assert cfg["enemies"]["Dragon"]["experience"]==75
