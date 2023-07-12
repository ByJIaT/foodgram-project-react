#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres..."

  while ! nc -z localhost 5432;
    do sleep 0.3
  done

  echo "Postgres started"
fi

python manage.py migrate
python manage.py load_json_data
gunicorn -w 2 -b 0:8000 config.wsgi

exec "$@"