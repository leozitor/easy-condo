FROM python:3

COPY .  /usr/src/app
# where your code lives
WORKDIR /usr/src/app
# run this command to install all dependencies
RUN apt-get -y install libz-dev libjpeg-dev libfreetype6-dev
RUN pip install -r requirements.txt
# Collect static files and Start server
CMD  ["/bin/bash", "-c", "python3 manage.py collectstatic --noinput &&  python3 manage.py runserver 0.0.0.0:80"]