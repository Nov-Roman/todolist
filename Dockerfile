FROM python:3.10-slim
RUN pip install --upgrade pip
RUN apt-get update \
    && apt-get -y install libpq-dev gcc\
    && pip install psycopg2
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./ .
