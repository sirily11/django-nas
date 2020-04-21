FROM python:3.7.5
RUN apt update -y
RUN apt install -y ffmpeg
RUN ffmpeg -version
WORKDIR /usr/local/django_nas
COPY requirements.txt requirements.txt
RUN apt-get install -y python-dev libxml2-dev
RUN apt-get install -y libxslt1-dev antiword unrtf poppler-utils tesseract-ocr
RUN apt-get install -y flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig
RUN pip3 install -r requirements.txt