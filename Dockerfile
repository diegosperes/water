from alpine:3.8

RUN apk update \
    && apk upgrade \
    && apk add make \
    && apk add python3 \
    && ln -fs pip3 /usr/bin/pip \
    && ln -fs /usr/bin/python3 /usr/bin/python \
    && pip install -U pip setuptools \
    && echo "Default python version: " `python --version`

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY ./Makefile /app/Makefile
RUN make setup

COPY . "/app"

CMD ["make", "start"]
