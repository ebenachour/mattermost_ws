From python:3.7-slim-stretch
WORKDIR /home/matterbot
RUN apt update && apt install make
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

