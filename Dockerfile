FROM python:3.8

RUN mkdir /app
WORKDIR /app

COPY ./backend/ /app/
RUN pip install pip==22.0.4
RUN pip install pipenv-to-requirements
RUN pipenv_to_requirements
RUN pip install -r requirements.txt

ENV POSTGRES_USER postgres
ENV POSTGRES_DB postgres