import pytest


def test_get_product_non_existent(test_client):
    response = test_client.delete('/products/0')
    assert response.status_code == 404, (
        'При попытке получить несуществующий продукт должен возвращаться '
        'статус-код 404.'
    )


def test_get_product(test_client, product_a_lot):
    response = test_client.get('/products/1')
    assert (
        response.status_code == 200
    ), (
        'При GET-запросе к эндпоинту `/products/1` должен возвращаться '
        'статус-код 200.'
    )
    assert isinstance(
        response.json(), dict
    ), (
        'При GET-запросе к эндпоинту `/products/1` должен возвращаться '
        'объект типа `dict`.'
    )
    keys = sorted(
        [
            'title',
            'description',
            'price',
            'quantity'
        ]
    )
    assert (
        sorted(list(response.json().keys())) == keys
    ), (
        'При GET-запросе к эндпоинту `/products/1` в ответе API должны '
        f'быть ключи `{keys}`.'
    )
    assert response.json() == {
        'title': 'chimichangas4life',
        'description': 'Huge fan of chimichangas. Wanna buy a lot',
        'price': 1000000,
        'quantity': 10000000,
    }, (
        'При GET-запросе к эндпоинту `/products/1` тело ответа API '
        'отличается от ожидаемого.'
    )


def test_get_products(test_client, product_a_lot, product_little):
    response = test_client.get('/products/')
    assert (
        response.status_code == 200
    ), (
        'При GET-запросе к эндпоинту `/products/` должен возвращаться '
        'статус-код 200.'
    )
    assert isinstance(
        response.json(), list
    ), (
        'При GET-запросе к эндпоинту `/products/` должен возвращаться '
        'объект типа `list`.'
    )
    assert len(response.json()) == 2, (
        'При корректном GET-запросе к эндпоинту `/products/` должны '
        'возвращаться объекты из БД. Проверьте модель `Product`.'
    )
    data = response.json()[0]
    keys = sorted(
        [
            'title',
            'description',
            'price',
            'quantity'
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), (
        'При GET-запросе к эндпоинту `/products/` в ответе API должны '
        f'быть ключи `{keys}`.'
    )
    assert response.json() == [
        {
            'title': 'chimichangas4life',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'price': 1000000,
            'quantity': 10000000,
        },
        {
            'title': 'nunchaku',
            'description': 'Nunchaku is better',
            'price': 5000000,
            'quantity': 0,
        }
    ], (
        'При GET-запросе к эндпоинту `/products/` тело ответа API '
        'отличается от ожидаемого.'
    )


def test_create_product(test_client):
    response = test_client.post(
        '/products/',
        json={
            'title': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'price': 1000000,
            'quantity': 1
        },
    )
    assert (
        response.status_code == 200
    ), 'При создании продукта должен возвращаться статус-код 200.'
    data = response.json()
    keys = sorted(
        [
            'title',
            'description',
            'price',
            'quantity'
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f'При создании продукта в ответе API должны быть ключи `{keys}`.'
    assert data == {
        'title': 'Мертвый Бассейн',
        'description': 'Deadpool inside',
        'price': 1000000,
        'quantity': 1
    }, 'При создании продукта тело ответа API отличается от ожидаемого.'


@pytest.mark.parametrize(
    'json',
    [
        {
            'title': 'Мертвый Бассейн',
            'quantity': '1000000',
        },
        {
            'description': 'Deadpool inside',
            'quantity': '1000000',
        },
        {
            'title': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
        },
        {
            'title': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'quantity': 'Donat',
        },
        {
            'title': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'quantity': '',
        },
        {},
    ],
)
def test_create_product_validation_error(json, test_client):
    response = test_client.post('/products/', json=json)
    assert response.status_code == 422, (
        'При некорректном создании продукта должен возвращаться '
        'статус-код 422.'
    )


def test_update_product(test_client, product_a_lot):
    response = test_client.put(
        f'/products/{product_a_lot.id}',
        json={
            'title': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'price': 1000000,
            'quantity': 1
        },
    )
    assert (
        response.status_code == 200
    ), 'При обновлении продукта должен возвращаться статус-код 200.'
    data = response.json()
    keys = sorted(
        [
            'title',
            'description',
            'price',
            'quantity'
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f'При обновлении продукта в ответе API должны быть ключи `{keys}`.'
    assert data == {
        'title': 'Мертвый Бассейн',
        'description': 'Deadpool inside',
        'price': 1000000,
        'quantity': 1
    }, 'При обновлении продукта тело ответа API отличается от ожидаемого.'


@pytest.mark.parametrize(
    'json',
    [
        {
            'title': 'Мертвый Бассейн',
            'quantity': '1000000',
        },
        {
            'description': 'Deadpool inside',
            'quantity': '1000000',
        },
        {
            'title': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
        },
        {
            'title': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'quantity': 'Donat',
        },
        {
            'title': 'Мертвый Бассейн',
            'description': 'Deadpool inside',
            'quantity': '',
        },
        {},
    ],
)
def test_update_product_validation_error(json, test_client, product_a_lot):
    response = test_client.put(f'/products/{product_a_lot.id}', json=json)
    assert response.status_code == 422, (
        'При некорректном обновлении продукта должен возвращаться '
        'статус-код 422.'
    )


def test_delete_product(test_client, product_a_lot):
    response = test_client.delete(f'/products/{product_a_lot.id}')
    assert response.status_code == 200, (
        'При попытке удалить продукт должен возвращаться статус-код 200.'
    )


def test_delete_product_non_existent(test_client):
    response = test_client.delete('/products/0')
    assert response.status_code == 404, (
        'При попытке удалить несуществующий продукт должен возвращаться'
        'статус-код 404.'
    )


def test_delete_product_in_order(test_client, order_item):
    response = test_client.delete(f'/products/{order_item.product_id}')
    assert response.status_code == 423, (
        'Добавленный в заказ продукт не может быть удален.'
    )
