#!/bin/bash

docker compose down --volumes --remove-orphans
docker compose up -d postgres

sleep 2

# rm -rf migrations pyproject.toml aerich.ini
# aerich init -t app.database.TORTOISE_ORM
# aerich init-db

# aerich migrate
# aerich upgrade

docker compose up -d backend