#!/bin/sh

python manage.py migrate
python manage.py load_json_data
python manage.py collectstatic --noinput
gunicorn -w 2 -b 0:8000 config.wsgi

exec "$@"