FROM python:3.10-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache bash
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add libffi-dev

WORKDIR /BookStore
COPY requirements.txt /BookStore/requirements.txt
RUN pip install -r requirements.txt
COPY . /BookStore


RUN chmod +x  /BookStore/entrypoints/wait-for-it.sh \
              /BookStore/entrypoints/start-backend.sh \
              /BookStore/entrypoints/start-celery.sh


# Default entrypoint (can be overridden by docker-compose or command line)
ENTRYPOINT ["/BookStore/entrypoints/start-backend.sh"]