FROM python:3.9.6-alpine3.14

WORKDIR /home/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip3 install --upgrade pip setuptools wheel
COPY ./requirements.txt /home/app/requirements.txt 
RUN chmod +x /home/app/requirements.txt
RUN pip install -r requirements.txt
COPY ./Django /home/app/