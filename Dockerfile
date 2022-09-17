# pull python
FROM python:3.10-alpine

# set workdir
RUN mkdir /code
WORKDIR /code

# copy project
COPY . /code/

# disable writing bytecode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN python manage.py collectstatic
