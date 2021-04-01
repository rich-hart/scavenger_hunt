from ubuntu:20.04

run apt-get update && apt-get install -y  \
        python3-dev \
        python3-pip \
	vim 

workdir /app

copy requirements.txt requirements.txt

run pip3 install -r requirements.txt

copy . .

cmd gunicorn --bind 0.0.0.0:8000 hunt.wsgi
