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

4. Запусти проект
    ```
    python manage.py runserver
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
   
# Пользователи
## Админ
E-Mail: admin@admin.com

Пароль: admin
