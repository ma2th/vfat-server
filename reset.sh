#!/bin/bash

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -path "*/__pycache__/*" -exec rm -rf {} \;

rm db.sqlite3

python manage.py makemigrations --settings=vfatserver.settings_debug
python manage.py makemigrations api assessment clientconf main stats train --settings=vfatserver.settings_debug
python manage.py migrate --settings=vfatserver.settings_debug
python manage.py collectstatic  --settings=vfatserver.settings_debug
python manage.py createsuperuser --settings=vfatserver.settings_debug

cat create_demo_user.py | python manage.py shell --settings=vfatserver.settings_debug
cat create_home_page.py | python manage.py shell --settings=vfatserver.settings_debug
















