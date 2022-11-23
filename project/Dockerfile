FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEPLOY_ENV=1

WORKDIR /usr/src/project

COPY ./remotecontrol ./remotecontrol

WORKDIR /usr/src/project/remotecontrol
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

CMD python manage.py makemigrations --noinput \
    && python manage.py migrate --noinput \
    && python manage.py runserver 0.0.0.0:8000 