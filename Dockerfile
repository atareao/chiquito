FROM alpine:3.13

ENV TZ=Europe/Madrid
MAINTAINER Lorenzo Carbonell <a.k.a. atareao> "lorenzo.carbonell.cerezo@gmail.com"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt

RUN echo "**** install Python ****" && \
    apk add --update --no-cache python3 tini tzdata && \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    echo "**** install dependencies **** " && \
    pip3 install --no-cache-dir -r /requirements.txt && \
    rm -rf /var/lib/apt/lists/* /requirements.txt && \
    echo "**** create user ****" && \
    addgroup dockeruser && \
    adduser -h /app -G dockeruser -D dockeruser && \
    mkdir -p /app/database && \
    chown -R dockeruser:dockeruser /app


WORKDIR /app
USER dockeruser
COPY start.sh /start.sh
COPY ./app /app

ENTRYPOINT ["tini", "--"]
CMD ["/bin/sh", "/start.sh"]
