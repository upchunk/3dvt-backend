#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

## Only run when first spin
python manage.py flush --no-input
python manage.py clearsessions
python manage.py flushexpiredtokens
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

exec "$@"