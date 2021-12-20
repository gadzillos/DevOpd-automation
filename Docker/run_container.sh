#!/bin/bash
# create persistent storage directory
mkdir -p $HOME/docker/volumes/postgres
docker run --rm --name docker_db -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/pgsql/14 docker_psql
