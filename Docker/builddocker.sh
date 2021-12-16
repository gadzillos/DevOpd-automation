#!/bin/bash
echo "Starting shell script"
sudo cd /opt/repo/Docker
echo "build the docker image"
sudo docker build -t docker_psql