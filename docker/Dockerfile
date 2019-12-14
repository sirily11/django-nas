FROM python:3.7.5
RUN apt update -y
RUN apt install -y ffmpeg
RUN ffmpeg -version
WORKDIR /usr/local/django_nas
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt