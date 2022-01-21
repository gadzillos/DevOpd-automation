#!/bin/bash
systemctl enable postgresql-12.service
systemctl start postgresql-12.service
sudo -u postgres bash << EOF
echo "In"
psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&
createdb -O docker docker
EOF
echo "Out"