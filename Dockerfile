# Python base
FROM python:3.9.6-slim

# Non-root user for better security
RUN useradd -ms /bin/bash memeuser

# Set the working directory
WORKDIR /memeTradingBot

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install dependencies, Chrome, and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    ca-certificates \
    curl \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && dpkg --info google-chrome-stable_current_amd64.deb | grep Version \
    && rm google-chrome-stable_current_amd64.deb \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set ownership to the non-root user
RUN chown -R memeuser:memeuser /memeTradingBot

# Switch to non-root user
USER memeuser

# Default command to run the application
CMD [ "python3", "./memecoinFeed.py" ]