.PHONY: $(MAKECMDGOALS)
.EXPORT_ALL_VARIABLES:

ifneq ($(DEBUG), true)
.SILENT:
endif


ORACLE_HOME       ?= "$(shell pwd)/$(shell find . -type d -name instantclient* -exec basename {} \;)"
DYLD_LIBRARY_PATH := $(ORACLE_HOME)
LD_LIBRARY_PATH   := $(ORACLE_HOME)
PATH              := $(ORACLE_HOME):$(PATH)

app:
	pipenv run python app.py

pyshell:
	pipenv shell

test:
	env | sort