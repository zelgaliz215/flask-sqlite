FROM alpine:3.20

RUN apk add --no-cache python3-dev

WORKDIR /app

COPY . /app/

RUN python3 -m venv env

RUN source env/bin/activate && pip install --no-cache-dir -r src/requirements.txt

EXPOSE 5000

CMD [ "sh", "-c", "source env/bin/activate && python src/app.py" ]

#docker ps
# docker build -t flask-docker-img .
# docker run --rm -p 5000:5000 flask-docker-img
#docker exec -it bd46fffb7029 ash
