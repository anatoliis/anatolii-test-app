FROM python:3.7.0-alpine

RUN apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev

ADD requirements.txt /

RUN set -ex && pip install -r requirements.txt

ADD . /

CMD ["/bin/sh", "/entrypoint.sh"]
