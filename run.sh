#!/bin/bash

python manage.py runserver --settings=vfatserver.settings_debug

# Open http://127.0.0.1:8000/home in browser