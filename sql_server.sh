#!/usr/bin/env bash

set -euo pipefail

sql_data="sql_data"

$(docker volume list | grep ${sql_data} 1>/dev/null) || \
  { printf "Data volume not found, creating: "; docker volume create ${sql_data}; }

docker run --rm \
--name oracle-db \
-p 1521:1521 -p 5500:5500 \
-e ORACLE_PWD=demopass \
-e ORACLE_CHARACTERSET=AL32UTF8 \
-v ${sql_data}:/opt/oracle/oradata \
container-registry.oracle.com/database/express:21.3.0-xe



# docker run --rm \
#   --name some-mariadb \
#   --env MARIADB_USER=example-user \
#   --env MARIADB_PASSWORD=my_cool_secret \
#   --env MARIADB_ROOT_PASSWORD=my-secret-pw \
#   mariadb:latest


# export ORACLE_HOME="$(pwd)/$(find . -type d -name instantclient* -exec basename {} \;)"
# export DYLD_LIBRARY_PATH=$ORACLE_HOME
# export LD_LIBRARY_PATH=$ORACLE_HOME
# export PATH=$ORACLE_HOME:$PATH