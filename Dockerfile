FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine-2020-12-19

WORKDIR /app

RUN pip install --install-option="--prefix=/install" Werkzeug

COPY ./app /app