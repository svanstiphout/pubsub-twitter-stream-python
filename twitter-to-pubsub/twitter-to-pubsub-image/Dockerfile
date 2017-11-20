FROM python:3

COPY twitter-to-pubsub.py /twitter-to-pubsub.py
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-u", "twitter-to-pubsub.py"]