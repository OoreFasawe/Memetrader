# Python base
FROM python:3.9.6-slim

# non-root user for better security
RUN useradd -ms /bin/bash memeuser

# Set the directory
WORKDIR /memeTradingBot

COPY requirements.txt requirements.txt

# Install dependencies and clean up (one step)
RUN apt-get update && apt-get install -y --no-install-recommends \
wget \
unzip \
ca-certificates \
curl \
&& wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
&& apt install -y ./google-chrome-stable_current_amd64.deb \
&& rm google-chrome-stable_current_amd64.deb \
&& apt-get clean && rm -rf /var/lib/apt/lists/* \
&& pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Set ownership to the non-root user
RUN chown -R memeuser:memeuser /memeTradingBot

# Switch to non-root user
USER memeuser

CMD [ "python3", "./memecoinFeed.py" ]