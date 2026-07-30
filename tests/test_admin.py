from src.models_db import User, UserRole, db


def test_non_admin_gets_403(client, make_user):
    make_user(email="user1@example.com", password="password123", role=UserRole.USER)
    client.post("/login", data={"email": "user1@example.com", "password": "password123"})
    response = client.get("/admin")
    assert response.status_code == 403


def test_admin_can_view_dashboard(client, make_user):
    make_user(email="admin1@example.com", password="password123", role=UserRole.ADMIN)
    client.post("/login", data={"email": "admin1@example.com", "password": "password123"})
    response = client.get("/admin")
    assert response.status_code == 200


def test_admin_cannot_delete_self(client, make_user):
    admin_id = make_user(email="admin2@example.com", password="password123", role=UserRole.ADMIN)
    client.post("/login", data={"email": "admin2@example.com", "password": "password123"})
    response = client.post(f"/admin/users/{admin_id}/delete")
    assert response.status_code == 400


def test_admin_can_delete_other_user(client, make_user, app):
    make_user(email="admin3@example.com", password="password123", role=UserRole.ADMIN)
    target_id = make_user(email="target@example.com", password="password123", role=UserRole.USER)
    client.post("/login", data={"email": "admin3@example.com", "password": "password123"})

    dashboard_page = client.get("/admin")
    csrf_token = dashboard_page.data.decode().split('name="csrf_token" value="')[1].split('"')[0]

    response = client.post(
        f"/admin/users/{target_id}/delete",
        data={"csrf_token": csrf_token},
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        assert db.session.get(User, target_id) is None
