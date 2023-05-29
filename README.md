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

# Пользователи
## Админ
E-Mail: admin@admin.com

Пароль: admin
