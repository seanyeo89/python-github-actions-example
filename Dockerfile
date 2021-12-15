FROM python:3.9-slim
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
CMD gunicorn -b 0.0.0.0:8080 src.app:server

#Docker
#1)docker run -d -p
#2)docker images
#3)docker ps show u containers
#4)docker log container-id
#5)docker kill $(docker ps -q)