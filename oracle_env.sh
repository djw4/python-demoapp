export ORACLE_HOME="$(pwd)/$(find . -type d -name instantclient* -exec basename {} \;)"
export DYLD_LIBRARY_PATH=$ORACLE_HOME
export LD_LIBRARY_PATH=$ORACLE_HOME
export PATH=$ORACLE_HOME:$PATH