FROM python:3.9.6-slim

WORKDIR /memeTradingBot

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y wget unzip ca-certificates curl && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

COPY . .
CMD [ "python3", "./memecoinFeed.py" ]