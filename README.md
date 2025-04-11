# Car Scraping API
!!!!
!!!!
!!!!
P.S (Дизайн та кількість елементів в парсингу не великий (10 автомобілів першої сторінки і супер елементарна сторінка, тільки через те, що тестове тоді вийде як готовий додаток і за це вже можна брати гроші)), якщо по тестовому ок, готовий покращити всі деталі!
!!!!
!!!!
!!!!
Цей проект є FastAPI додатком для збору, зберігання та надання інформації про автомобілі. Він дозволяє користувачам отримувати інформацію про автомобілі, додавати нові автомобілі до бази даних, оновлювати існуючі записи, а також здійснювати скрапінг даних про автомобілі з інших джерел.

## Інструкції з налаштування

### Крок 1: Клонування репозиторію


Клонуйте репозиторій:
```bash
git clone https://github.com/yourusername/car-scraping-api.git](https://github.com/tr1cky192/car_scraper_api.git
cd car-scraping-api

```
### Крок 2: Створення віртуального середовища
Створіть віртуальне середовище:
python3 -m venv venv

### Крок 3: Встановлення залежностей
Встановіть необхідні залежності:
pip install -r requirements.txt

Крок 4: Налаштування MongoDB
Переконайтесь, що у вас є запущена база даних MongoDB на локальній машині або на віддаленому сервері. Використовуйте URI для підключення до вашої бази даних.
Крок 5: Запуск проекту
Запустіть сервер:
uvicorn app.main:app --reload
Може бути python -m uvicorn app.main:app
(або захоче pip install unicorn)

## Документація по API
1. Аутентифікація
POST /token
Запит на отримання токену доступу.
curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=test&password=password'
Відповідь:
{
  "access_token": "your_token",
  "token_type": "bearer"
}

2. Створення автомобіля
POST /cars
Створює новий запис про автомобіль у базі даних.
curl -X 'POST' \
  'http://127.0.0.1:8000/cars' \
  -H 'Authorization: Bearer <your_token>' \
  -H 'Content-Type: application/json' \
  -d '{
        "make": "Toyota",
        "model": "Corolla",
        "year": 2020,
        "price": 20000,
        "mileage": 15000,
        "image_url": "http://example.com/car.jpg"
      }'

3. Отримання списку автомобілів
GET /cars
Отримує список автомобілів з можливістю фільтрації та сортування.
Параметри запиту:
skip: кількість пропущених елементів.
limit: кількість елементів для виведення.
min_price: мінімальна ціна.
max_price: максимальна ціна.
min_mileage: мінімальний пробіг.
max_mileage: максимальний пробіг.
sort_by: параметр сортування (ціна, рік, пробіг).
sort_order: порядок сортування (asc, desc).

curl -X 'GET' \
  'http://127.0.0.1:8000/cars?min_price=5000&max_price=30000&sort_by=price&sort_order=asc' \
  -H 'Authorization: Bearer <your_token>'


4. Оновлення автомобіля
PUT /cars/{car_id}
Оновлює дані про автомобіль за його ID.
curl -X 'PUT' \
  'http://127.0.0.1:8000/cars/60c72b2f9e7f8b001f5b9f1e' \
  -H 'Authorization: Bearer <your_token>' \
  -H 'Content-Type: application/json' \
  -d '{
        "make": "Toyota",
        "model": "Corolla",
        "year": 2021,
        "price": 21000,
        "mileage": 12000,
        "image_url": "http://example.com/car_updated.jpg"
      }'


5. Видалення автомобіля
DELETE /cars/{car_id}
Видаляє автомобіль за його ID.

curl -X 'DELETE' \
  'http://127.0.0.1:8000/cars/60c72b2f9e7f8b001f5b9f1e' \
  -H 'Authorization: Bearer <your_token>'


