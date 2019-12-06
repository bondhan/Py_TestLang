FROM python:3.7-alpine

ADD . /app

WORKDIR /app

ENV MYSQL_DSN="mysql+mysqldb://tx-python:tUlJ3475@192.168.48.20:3306/pylang_db" \
	WORKER_NUM="10" \
	LISTEN_ADDR="0.0.0.0" \
	PATH="/app/env/bin:$PATH" \
	VIRTUAL_ENV="/app/env"

RUN apk add --no-cache --no-progress -q \
	mariadb-connector-c-dev \
	libffi-dev \
	musl-dev \
	mysql-client \
	postgresql-dev \
	gcc

RUN pip install virtualenv --no-cache-dir -q && \
	virtualenv env

RUN . env/bin/activate && \
	pip install -r requirements.txt --no-cache-dir --disable-pip-version-check -q

ENTRYPOINT ["./docker-entrypoint.sh"]

EXPOSE 5000

CMD ["/bin/sh", "run_pytestlang.sh"]