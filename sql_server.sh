#!/usr/bin/env bash

set -euo pipefail

sql_data="sql_data"
mysql_tag="mariadb:10.8.5-jammy"

$(docker ps | grep mariadb 1>/dev/null) && docker stop mariadb
docker container prune -f

$(docker volume list | grep ${sql_data} 1>/dev/null) || \
  { printf "Data volume not found, creating: "; docker volume create ${sql_data}; }

docker run \
  --name mariadb \
  --detach \
  --env-file .env \
  --restart unless-stopped \
  --volume sql_data:/var/lib/mysql \
  --publish 3306:3306 \
  mariadb:10.8.5-jammy


# TODO: Use the oracle container for testing legacy migrations
# docker run --rm \
# --name oracle-db \
# -p 1521:1521 -p 5500:5500 \
# -e ORACLE_PWD=demopass \
# -e ORACLE_CHARACTERSET=AL32UTF8 \
# -v ${sql_data}:/opt/oracle/oradata \
# container-registry.oracle.com/database/express:21.3.0-xe