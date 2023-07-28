

def test_read_menus(client, db_session, test_menu):
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []

    db_session.add(test_menu)
    db_session.commit()

    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['title'] == test_menu.title


def test_read_menu(client, db_session, test_menu):
    db_session.add(test_menu)
    db_session.commit()

    response = client.get(f"/api/v1/menus/{test_menu.id}")
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == test_menu.title
    assert data['description'] == test_menu.description


def test_read_not_exist_menu(client, db_session):
    response = client.get(f"/api/v1/menus/8000000")
    assert response.status_code == 404


def test_create_menu(client):
    menu_data = {"title": "New Menu", "description": "New Description"}
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == menu_data['title']
    assert data['description'] == menu_data['description']


def test_update_menu(client, db_session, test_menu):
    db_session.add(test_menu)
    db_session.commit()

    updated_data = {"title": "Updated Title", "description": "Updated Description"}
    response = client.patch(f"/api/v1/menus/{test_menu.id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == updated_data['title']
    assert data['description'] == updated_data['description']


def test_update_not_exist_menu(client, db_session):
    updated_data = {"title": "Updated Title", "description": "Updated Description"}
    response = client.patch(f"/api/v1/menus/{800000000}", json=updated_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Menu not found'}


def test_delete_menu(client, db_session, test_menu):
    db_session.add(test_menu)
    db_session.commit()

    response = client.delete(f"/api/v1/menus/{test_menu.id}")
    assert response.status_code == 200
    assert response.json() == {"status": True, "message": "Menu deleted"}
