# Ads-Project

---Небольшое приложение для бесплатных объявлений---

Для запуска проекта установите python версии 3.9.11 и pip

После клонирования перейдите в склонированную папку и выполните следующие команды:

Создайте виртуальное окружение командой
```bash
python -m venv venv
```

Активируйте виртуальное окружение командой
```bash
source venv/bin/activate
или
venv\Scripts\activate (для Windows)
```

Установите зависимости командой

```bash
pip install -r requirements.txt
```

Примените миграции командой
```bash
./manage.py migrate
```

Загрузите фикстурные статьи командой
```bash
./manage.py loaddata fixtures/auth.json
./manage.py loaddata fixtures/dump.json
```

Создайте в PostgreSQL базу данных, а затем в директории с проектом создайте файл .env и заполните по примеру:


SECRET_KEY=django_secret_key

DEBUG=(1 for True, 0 for False)

POSTGRES_DB=db_name

POSTGRES_USER=db_user_name

POSTGRES_PASSWORD=db_user_password

POSTGRES_PORT=db_port

POSTGRES_HOST=db_host


Чтобы запустить сервер выполните:

```bash
./manage.py runserver
```

Для доступа в панель администратора перейдите по ссылке http://localhost:8000/admin
(пароли созданных юзеров соответсвуют их юзернеймам)