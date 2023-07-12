#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres..."

  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT;
    do sleep 0.1
  done

  echo "Postgres started"
fi

python manage.py migrate
python manage.py load_json_data
gunicorn -w 2 -b 0:8000 config.wsgi

exec "$@"