import jsonschema
import pytest

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "active"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "active": {"type": "boolean"},
    },
}


@pytest.mark.api
@pytest.mark.smoke
def test_health(api_client):
    r = api_client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.api
def test_get_user_matches_schema(api_client):
    r = api_client.get("/users/1")
    assert r.status_code == 200
    jsonschema.validate(r.json(), USER_SCHEMA)


@pytest.mark.api
def test_user_not_found(api_client):
    assert api_client.get("/users/0").status_code == 404


@pytest.mark.api
def test_login_success(api_client):
    r = api_client.post("/login", json={"username": "admin", "password": "123456"})
    assert r.status_code == 200
    assert r.json()["token"]


@pytest.mark.api
def test_login_wrong_password(api_client):
    r = api_client.post("/login", json={"username": "admin", "password": "wrong"})
    assert r.status_code == 401
