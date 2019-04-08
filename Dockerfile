FROM python:3.7
RUN apt-get update && \
        apt-get install -y libopus0 ffmpeg
ADD . /bot
WORKDIR /bot
RUN pip install -r requirements.txt
CMD ["python", "-u", "bot.py"]

