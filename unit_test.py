import pytest

from api import API

@pytest.fixture
def api():
    return API()

@pytest.fixture
def client(api):
    return api.test_session()

def test_bumbo_test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @api.pathway("/hey")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get("http://ion/hey").text == RESPONSE_TEXT

def test_parameterized_route(api, client):
    @api.pathway("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://ion/matthew").text == "hey matthew"
    assert client.get("http://ion/ashley").text == "hey ashley"

def test_default_404_response(client):
    response = client.get("http://ion/doesnotexist")

    assert response.status_code == 404
    assert response.text == "Unknown page"

def test_alternative_route(api, client):
    response_text = "Alternative way to add a route"

    def home(req, resp):
        resp.text = response_text

    api.add_pathway("/alternative", home)

    assert client.get("http://ion/alternative").text == response_text