import pytest
from conftest import app, get_async_session, override_db
from fastapi.testclient import TestClient


@pytest.fixture
def product_a_lot(mixer):
    return mixer.blend(
        'app.models.product.Product',
        title='chimichangas4life',
        description='Huge fan of chimichangas. Wanna buy a lot',
        price=1000000,
        quantity=10000000,
    )


@pytest.fixture
def product_little(mixer):
    return mixer.blend(
        'app.models.product.Product',
        title='nunchaku',
        description='Nunchaku is better',
        price=5000000,
        quantity=0,
    )


@pytest.fixture
def order(mixer):
    # TODO: freezer
    return mixer.blend('app.models.order.Order')


@pytest.fixture
def order_item(mixer, product_a_lot, order):
    return mixer.blend(
        'app.models.order_item.OrderItem',
        product_id=product_a_lot.id,
        order_id=order.id,
        quantity=10
    )


@pytest.fixture
def test_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    with TestClient(app) as client:
        yield client
