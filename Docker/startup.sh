#!/bin/bash
systemctl enable postgresql-14.service
systemctl start postgresql-14.service
-u postgres bash << EOF
echo "In"
psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&
createdb -O docker docker
EOF
echo "Out"