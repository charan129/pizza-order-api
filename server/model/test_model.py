import pytest
from data_model import Order


@pytest.fixture()
def new_order():
    order = Order("481024024h534508b1b2m329", {
        "Order": ["pizzzzza1", "pizzzzza2"]})
    return order


def test_new_order(new_order):
    assert new_order._id == "481024024h534508b1b2m329"
    assert new_order.data == {"Order": ["pizzzzza1", "pizzzzza2"]}
