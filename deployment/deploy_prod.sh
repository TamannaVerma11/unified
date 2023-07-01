#!/bin/sh

ssh root@156.67.220.117 /bin/bash <<EOF
  cd unified
  git pull
  source env/bin/activate
  python manage.py makemigrations
  python manage.py migrate  --run-syncdb
  sudo service gunicorn restart
  sudo service nginx restart
  exit
EOF
