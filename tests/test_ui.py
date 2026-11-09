def test_ui(client):
    r=client.get("/"); assert r.status_code==200; assert "Character Adventure" in r.text; assert 'id="character-form"' in r.text
    js=client.get("/static/app.js"); assert js.status_code==200; assert 'fetch("/characters"' in js.text; assert 'method:"POST"' in js.text
