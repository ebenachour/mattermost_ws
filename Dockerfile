From python:3.7-slim-stretch
WORKDIR /home/matterbot
ENV MAT_URL="tata" MAT_LOGIN="ett" MAT_PWD="pass" MAT_PORT=442
RUN apt-get update && apt-get -y install make
COPY requirements.txt requirements-dev.txt /home/matterbot/
RUN pip install -r requirements.txt -r requirements-dev.txt
COPY . .
ENTRYPOINT ["make"]
