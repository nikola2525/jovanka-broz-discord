FROM python:3.7-slim
RUN apt-get update && \
        apt-get -y install \
        libopus0 ffmpeg \
        && rm -rf /var/lib/apt/lists/*
WORKDIR /bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src ./src
CMD ["python", "-u", "src/bot.py"]

