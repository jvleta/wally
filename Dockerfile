FROM python:3.11.8-slim-bookworm

WORKDIR /app

COPY . .

RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e . && pip cache purge

ENV FLASK_APP=flaskapp/main.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]