.PHONY: $(MAKECMDGOALS)
.EXPORT_ALL_VARIABLES:

ifneq ($(DEBUG), true)
.SILENT:
endif


# ORACLE_HOME       ?= "$(shell pwd)/$(shell find . -type d -name instantclient* -exec basename {} \;)"
# DYLD_LIBRARY_PATH := $(ORACLE_HOME)
# LD_LIBRARY_PATH   := $(ORACLE_HOME)
# PATH              := $(ORACLE_HOME):$(PATH)

MARIADB_DATABASE      := demoapp
MARIADB_USER          := demoapp-user
MARIADB_PASSWORD      := demoapp
MARIADB_ROOT_PASSWORD := demoapp

app:
	pipenv run python app.py

pyshell:
	pipenv shell

.env:
	echo MARIADB_DATABASE=$(MARIADB_DATABASE) | tee .env
	echo MARIADB_USER=$(MARIADB_USER) | tee -a .env
	echo MARIADB_PASSWORD=$(MARIADB_PASSWORD) | tee -a .env
	echo MARIADB_ROOT_PASSWORD=$(MARIADB_ROOT_PASSWORD) | tee -a .env
	echo SECRET_KEY=$(shell openssl rand -hex 12) | tee -a .env

_URI_SQLITE  ?= sqlite:///students.sqlite3
_URI_MARIADB ?= mysql://root:$(MARIADB_ROOT_PASSWORD)@127.0.0.1/$(MARIADB_DATABASE)

_reset-uri:
	sed -i.backup '/^SQLALCHEMY_DATABASE_URI=.*/d' .env
	rm -f .env.backup

set-sqlite: _reset-uri
	echo SQLALCHEMY_DATABASE_URI="$(_URI_SQLITE)" | tee -a .env

set-mariadb: _reset-uri
	echo SQLALCHEMY_DATABASE_URI="$(_URI_MARIADB)" | tee -a .env
