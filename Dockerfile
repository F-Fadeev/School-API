FROM python:3.11.1-slim-buster
RUN apt-get update && apt-get install -y \
    && apt-get install libpq-dev python-dev build-essential gcc -y
WORKDIR /python_app
COPY req.txt req.txt
RUN pip install -r req.txt
COPY . .
EXPOSE 8000

