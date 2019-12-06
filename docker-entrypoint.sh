#!/bin/sh

sed -i "s#mysql+mysqldb://root:password@localhost:3306/pylang_db#$MYSQL_DSN#g" \
	src/config/flask_config_isoclient.py
sed -i "s#mysql+mysqldb://root:password@localhost:3306/pylang_db#$MYSQL_DSN#g" \
	src/config/flask_config_apiserver.py

exec "$@"