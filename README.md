# API для управления складом

## Тестовое задание "Effective Mobile"

<details open>
  <summary>Оглавление</summary>
  <ul>
    <li><a href="#описание">Описание</a></li>
    <li><a href="#настройка">Настройка</a></li>
    <li><a href="#запуск">Запуск</a></li>
    <li><a href="#требования">Требования</a></li>
  </ul>
</details>

## [Описание](#описание)

REST API с использованием FastAPI для управления процессами на складе.

## [Настройка](#настройка)

Шаблон заполнения `.env`:

```dotenv
DEBUG=True
DB_HOST=postgres
DB_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
APP_PORT=8000
```

## [Запуск](#запуск)

Запустите сервис и его инфраструктуру командой:

```
docker-compose -f infra/docker-compose.yml up -d
```

## [Требования](#требования)

### Основные требования:

- [x] Использовать SQLAlchemy (2 версии) для взаимодействия с базой данных.
- [x] Спроектировать таблицы для следующих сущностей:
    -  Product (Товар): id, название, описание, цена, количество на складе.
    -  Order (Заказ): id, дата создания, статус (напр. "в процессе", "отправлен", "доставлен").
    -  OrderItem (Элемент заказа): id, id заказа, id товара, количество товара в заказе.
- [x] Реализация REST API:
    - Эндпоинты для товаров:
        - Создание товара (POST /products).
        - Получение списка товаров (GET /products).
        - Получение информации о товаре по id (GET /products/{id}).
        - Обновление информации о товаре (PUT /products/{id}).
        - Удаление товара (DELETE /products/{id}).
    - Эндпоинты для заказов:
        - Создание заказа (POST /orders).
        - Получение списка заказов (GET /orders).
        - Получение информации о заказе по id (GET /orders/{id}).
        - Обновление статуса заказа (PATCH /orders/{id}/status).
- [x] Бизнес-логика:
    - При создании заказа проверять наличие достаточного количества товара на складе.
    - Обновлять количество товара на складе при создании заказа (уменьшение доступного количества).
    - В случае недостаточного количества товара – возвращать ошибку с соответствующим сообщением.
- [x] Документация:
    - Использовать встроенную документацию FastAPI (Swagger/OpenAPI).

### Дополнительные требования

- [x] Тестирование:
    - Написать несколько тестов с использованием pytest для проверки основных функций API.
- [x] Docker:
    - Создать Dockerfile и docker-compose файл для запуска проекта вместе с базой данных (например, PostgreSQL).
