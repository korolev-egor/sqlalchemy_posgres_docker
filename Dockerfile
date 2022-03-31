FROM python:3

WORKDIR /usr/src/app
RUN apt-get update
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app/
WORKDIR /usr/src/app/scripts
EXPOSE 5432
CMD sleep 3 ; python database.py ; tail -f /dev/null