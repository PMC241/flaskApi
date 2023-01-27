FROM python:3.10-alpine
EXPOSE 5000
WORKDIR /app
COPY . /app
RUN apk update && apk add gcc musl-dev mariadb-connector-c-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "main.py" ] 