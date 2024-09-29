import pytest


def test_get_order_non_existent(test_client):
    response = test_client.get('/orders/0')
    assert response.status_code == 404, (
        'При попытке получить несуществующий заказ должен возвращаться '
        'статус-код 404.'
    )


def test_get_order(test_client, order_item):
    response = test_client.get(f'/orders/{order_item.order.id}')
    assert (
        response.status_code == 200
    ), (
        f'При GET-запросе к эндпоинту `/orders/{order_item.order.id}` должен '
        'возвращаться статус-код 200.'
    )
    assert isinstance(
        response.json(), dict
    ), (
        f'При GET-запросе к эндпоинту `/orders/{order_item.order.id}` должен '
        'возвращаться объект типа `dict`.'
    )
    keys = sorted(
        [
            'id',
            'status',
            'created_at',
            'items',
        ]
    )
    assert (
        sorted(list(response.json().keys())) == keys
    ), (
        f'При GET-запросе к эндпоинту `/orders/{order_item.order.id}` в '
        f'ответе API должны быть ключи `{keys}`.'
    )
    data = response.json()
    data.pop('created_at')
    assert data == {
        'id': order_item.order.id,
        'status': 'in progress',
        'items': [{
            "product_id": order_item.product_id,
            "quantity": order_item.quantity,
        }],
    }, (
        f'При GET-запросе к эндпоинту `/orders/{order_item.order.id}` тело '
        'ответа API отличается от ожидаемого.'
    )


def test_get_orders(test_client, order):
    response = test_client.get('/orders/')
    assert (
        response.status_code == 200
    ), (
        'При GET-запросе к эндпоинту `/orders/` должен возвращаться '
        'статус-код 200.'
    )
    assert isinstance(
        response.json(), list
    ), (
        'При GET-запросе к эндпоинту `/orders/` должен возвращаться объект '
        'типа `list`.'
    )
    data = response.json()[0]
    keys = sorted(
        [
            'id',
            'status',
            'created_at'
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), (
        f'При GET-запросе к эндпоинту `/orders/` в '
        f'ответе API должны быть ключи `{keys}`.'
    )
    data.pop('created_at')
    assert data == {
        'id': order.id,
        'status': 'in progress'
    }, (
        'При GET-запросе к эндпоинту `/orders/` тело ответа API '
        'отличается от ожидаемого.'
    )


def test_create_order(test_client, product_a_lot):
    response = test_client.post(
        '/orders/',
        json=[
            {
                'product_id': product_a_lot.id,
                'quantity': 1
            }
        ],
    )
    assert (
        response.status_code == 200
    ), 'При создании заказа должен возвращаться статус-код 200.'
    data = response.json()
    keys = sorted(
        [
            'id',
            'status',
            'created_at'
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f'При создании заказа в ответе API должны быть ключи `{keys}`.'
    data.pop('created_at')
    assert data == {
        'id': 1,
        'status': 'in progress'
    }, 'При создании заказа тело ответа API отличается от ожидаемого.'


@pytest.mark.parametrize(
    'json',
    [
        {
            'product_id': 'Мертвый Бассейн',
            'quantity': '1000000',
        },
        {
            'product_id': 'Deadpool inside',
        },
        {
            'quantity': 'Мертвый Бассейн',
        },
        {
            'product_id': 0,
            'quantity': 'Donat',
        },
        {
            'product_id': '',
            'quantity': '',
        },
        {},
    ],
)
def test_create_product_validation_error(json, test_client):
    response = test_client.post('/orders/', json=json)
    assert response.status_code == 422, (
        'При некорректном создании заказа должен возвращаться '
        'статус-код 422.'
    )


@pytest.mark.parametrize(
    'json',
    [
        {'status': 'in progress'},
        {'status': 'sent'},
        {'status': 'delivered'}
    ]
)
def test_patch_product(json, test_client, order):
    response = test_client.patch(f'/orders/{order.id}', params=json)
    assert (
        response.status_code == 200
    ), 'При обновлении заказа должен возвращаться статус-код 200.'
    data = response.json()
    keys = sorted(
        [
            'id',
            'status',
            'created_at'
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f'При обновлении заказа в ответе API должны быть ключи `{keys}`.'
    data.pop('created_at')
    assert data == {
        'id': order.id,
        'status': json['status']
    }, 'При обновлении заказа тело ответа API отличается от ожидаемого.'


@pytest.mark.parametrize(
    'json',
    [
        {'status': ''},
        {'status': 1},
        {'status': 'Deadpool inside'},
        {},
    ],
)
def test_update_order_validation_error(json, test_client, order):
    response = test_client.patch(f'/orders/{order.id}', params=json)
    assert response.status_code == 422, (
        'При некорректном обновлении заказа должен возвращаться '
        'статус-код 422.'
    )


@pytest.mark.parametrize(
    'json',
    [
        {'status': 'in progress'},
        {'status': 'sent'},
        {'status': 'delivered'}
    ],
)
def test_update_order_non_existent(json, test_client):
    response = test_client.patch('/orders/0', params=json)
    assert response.status_code == 404, (
        'При обновлении несуществующего заказа должен возвращаться '
        'статус-код 404.'
    )
