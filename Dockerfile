FROM python:3.7

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV FLASK_APP run.py
ENV FLASK_ENV development

ENV AWS_DEFAULT_REGION eu-west-1

COPY . .
ENTRYPOINT ["/usr/local/bin/flask", "run", "--host=0.0.0.0"]
