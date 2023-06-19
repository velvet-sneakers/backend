# Инструкция по запуску проекта
1. Нужно создать виртуальное окружение
    ```
    python -m venv venv
    ```

2. Теперь нужно активировать виртуальное окружение

    Для Linux и Mac:
    ```
    source venv/bin/activate
    ```

    Для Windows:
    ```
    venv\Scripts\activate
    ```

3. Установи все нужные зависимости:
    ```
    pip install -r requirements.txt
    ```
   
4. Проведи миграцию:
    ```
    python manage.py migrate
    ```
   или
   ```
    venv/bin/python manage.py migrate
    ```

5. Запусти проект
    ```
    python manage.py runserver
    ```
   или 
   ```
    venv/bin/python manage.py runserver
    ```

## Fixtures
1. Создать фикстуру:
   ```
   python manage.py dumpdata product --indent 2 --output product/fixtures/products.json
   ```
2. Использовать фикстуру:
   ```
   python manage.py loaddata products
   ```
   
## Mailhog
1. Устанавливаем docker с официального сайта: https://docs.docker.com/desktop/
2. Запускаем Docker Desktop
3. Устанавливаем и сразу запускаем контейнер, пробрасывая порты
   ```
   docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
   ```
4. Переходим по адресу `http://localhost:8025`, где будет находиться админка Mailhog с сообщениями
   
## Docker Compose
1. Устанавливаем docker-compose с официального сайта: https://docs.docker.com/compose/install/
2. Убедитесь, что вы находитесь в папке проекта.
3. Запустите следующую команду:
   ```
   docker-compose up -d
   ```
4. Теперь бэкенд крутится на 8000 порту, а админка `Mailhog` на 8025 порту.

## Redis
Устанавливаем Redis
```
brew install redis
```
```
brew services start redis
```
Запускаем Redis сервер
```
redis-server
```

## Celery и Flower
Устанавливаем все новые зависимости в проекте
```
pip install -r requirements.txt
```
Запуск Celery (в отдельном терминале)
```
celery -A core worker --loglevel=info
```
Запускаем Flower (в отдельном терминале)
```
celery -A core flower --port=5555
```
По адресу http://localhost:5555 будет работать админка Flower, где будут отображаться задачи из `Celery`

## Как писать задачи для Celery
В папке приложения создайте файл `tasks.py`, где будут все задачи для `Celery` для конкретного приложения. Мы будем отправлять письма через Celery. Пример:
```python
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_created_shoes(name):
    send_mail(
        'Создана новая обувь',
        f'Создана обувь с именем {name}',
        'admin1@gmail.com',
        ['admin2@gmail.com'],
        fail_silently=True
    )
```

Теперь в `views.py` вызываем нашу функцию, которая принмает название обуви и отправляет письмо через `Celery`:
```python
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        send_email_created_shoes.delay(response.data.get("name"))

        return response
```

После того как вы создали новую задачу в `tasks.py`, нужно перезапускать `Celery` и `Flower`

Перезапуск Celery (в отдельном терминале)
```
celery -A core worker --loglevel=info
```
Перезапускаем Flower (в отдельном терминале)
```
celery -A core flower --port=5555
```

## Как сделать кеширование в Redis
Устанавливаем все новые зависимости в проекте
```
pip install -r requirements.txt
```
Далее заходим во `views.py` и для каждого запроса который нам нужен делаем так ->  
```python
from django.core.cache import cache

# Для создания
@action(methods=['POST'],detail= False, url_path="create-items")
    def create_items(self, request):
        serializer = self.serializer_class(data=request.data)
        # Остальной код
        
        # Добавляем данные в кеш
        cache.set(f'shop_item_{serializer.data.get("id")}', serializer.data, timeout=3600)
        
@action(methods=['GET'], detail=False, url_path="items")
    def get_items(self, request):
        # Пытаемся получить данные из кеша
        data = cache.get('shop_items')
        if not data:
            print("Fetching data from the database")
            # Если данных в кеше нет, то получаем их из базы данных и добавляем в кеш
            items = ShopItems.objects.all()
            data = ShopItemsSerializer(items, many=True).data
            cache.set('shop_items', data, timeout=3600)
        else:
            #Когда сделаете удалите принты для проверки
            print("Fetching data from cache")

        return Response(data)
```
Аналогично для `"PUT", "DELETE"` 
```python
# Обновляем данные в кеше
        cache.set(f'shop_item_{serializer.data.get("id")}', serializer.data, timeout=3600)

# Удаляем данные из кеша
        cache.delete(f'shop_item_{pk}')
```
Теперь проверяем:
1. в 1 терминале запускаем сервер
2. во 2 терминале запускаем `redis-server`

Теперь создаем(если нету) или получаем из бд предмет на сайте, принты в 1 термин. покажут что происходит.

3. в 3 терминале в самом конце проверим ключи - `redis-cli keys "*"`. 
Там должен будет появиться ключ с названием из строки `cache.get(f'shop_item_{pk}')`. Например у меня `shop_item`

# Пользователи
## Админ
E-Mail: admin@admin.com

Пароль: admin

