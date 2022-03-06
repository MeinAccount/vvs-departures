FROM python:3

EXPOSE 8000
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "-k", "gevent", "main:app" ]

ENV FLASK_APP=main.py
RUN flask assets build
