FROM python:3.10-alpine
EXPOSE 5000
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "main.py" ] 