def test_create_user(client):
    test_data = {"email": "ping@fastapitutorial.com", "password": "supersecret"}
    response = client.post("/users/", json=test_data)
    
    assert response.status_code==201
    assert response.json()["email"]=="ping@fastapitutorial.com"    