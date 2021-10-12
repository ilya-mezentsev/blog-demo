FROM ubuntu:20.10

RUN apt-get update && apt-get install -y \
  make \
  htop \
  python3 \
  python3-dev \
  python3-pip

RUN pip install virtualenv

WORKDIR /var/www
