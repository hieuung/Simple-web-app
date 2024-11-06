FROM python:3.9.18-bullseye

RUN apt-get update -y && \
    apt-get install pkg-config -y && \
    apt-get install python3-dev default-libmysqlclient-dev build-essential -y

RUN apt update -y && \
    apt install nginx -y

RUN mkdir -p /var/www/hieuut-bookstore

COPY . /var/www/hieuut-bookstore

WORKDIR /var/www/hieuut-bookstore

RUN pip install --upgrade pip && \ 
    pip install -r requirements.txt && \
    pip install flask[async]

COPY docker-entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/docker-entrypoint.sh 

ENTRYPOINT ["docker-entrypoint.sh"]