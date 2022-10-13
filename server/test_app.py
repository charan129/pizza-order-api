from typing import Dict
import pytest
from app import app


@pytest.fixture
def client():
    return app.test_client()


def test_welcome(client):
    # testing the welcome route by checking status code and response received
    res = client.get("/welcome")
    assert res.status_code == 200
    assert isinstance(res.text, str)
    assert res.text == "Welcome to Pizza House"


def test_order(client):
    # testing the order route by checking status code and response received
    res = client.post('/order', json={"order": ["p1", "p2"]})
    assert res.status_code == 201
    assert isinstance(res.get_json(force=True), Dict)
    assert res.get_json(force=True).get("Order ID")


def test_getorders(client):
    # testing the getorders route by checking status code and response received
    res = client.get("/getorders")
    assert res.status_code == 200
    assert isinstance(res.get_json(force=True), list)


def test_getspecificeorder(client):
    # testing the getorders/<order> route by checking status code and response received
    res = client.get("/getorders/24698326492934293873")
    assert res.status_code == 404
    assert res.text == "Not Found"


def test_getspecificeorder(client):
    # using the order_id received from order route to test the getorders/<order>
    res_order = client.post('/order', json={"order": ["p1", "p2"]})
    assert res_order.status_code == 201
    res = client.get(
        "/getorders/{}".format(res_order.get_json(force=True).get("Order ID")))
    assert res.status_code == 200
    assert len(res.get_json(force=True)) == 1
