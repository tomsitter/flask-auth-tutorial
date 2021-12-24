FROM python:3.8.2-slim-buster


LABEL org.tomsitter.com.authors="thomas.sitter@gmail.com"

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && \
    apt-get install -y netcat

# We copy just the requirements.txt first to leverage Docker cache
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]

# CMD [ "flask", "run" ]