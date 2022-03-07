FROM python:3

EXPOSE 8000
WORKDIR /app
VOLUME /static
ENV FLASK_APP=main.py

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
CMD flask assets build; cp -r static/* /static; gunicorn --bind 0.0.0.0:8000 -k gevent main:app
