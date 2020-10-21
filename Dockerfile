FROM python:3.8-slim-buster
LABEL maintainer="Adam Kielar"

RUN mkdir /app
WORKDIR /app

RUN addgroup --system user && adduser --system --no-create-home --group user
RUN chown -R user:user /app && chmod -R 755 /app

## install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt

USER user
COPY ./app /app