#!/bin/bash
systemctl enable postgresql-14.service
systemctl start postgresql-14.service
sudo su postgres
psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&
createdb -O docker docker
