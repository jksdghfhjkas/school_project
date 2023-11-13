# school_project
школьный проект 10 - 11 класс

Для запуска:

Виртуальное окружение
""""""cmd""""""""""
python -m venv venv
cd venv/Scripts
activate
"""""""""""""""""""
cd ../../
cd weather
pip install -r requirements.txt
"""""""""""""""""""""

Дальще в settings.py установите secret_key
В weatherapp/views.py установите token_api_openweather и token_api_yandex

Дальше
""""""cmd"""""""""
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
"""""""""""""""""""

