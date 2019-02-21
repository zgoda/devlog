FROM python:3.7-alpine

RUN apk --no-cache add \
    bash build-base \
    libffi-dev postgresql-dev

ADD devlog /app/devlog/
COPY requirements*.txt manage.py /app/

WORKDIR /app

RUN pip install -U pip && \
    pip install -U gunicorn psycopg2 && \
    pip install -U -r requirements-dev.txt

ENV IN_CONTAINER=yes
ENV FLASK_ENV=development
ENV AUTHLIB_INSECURE_TRANSPORT=1

ENTRYPOINT ["gunicorn", "--access-logfile", "-", "--reload", "devlog.wsgi:application", "--bind=0.0.0.0:5000"]
