#FROM python:3.13.0
FROM python:3.11.10-bookworm
LABEL maintainer="gafarov@realnoevremya.ru"
EXPOSE 8001
COPY main.py .
RUN apt-get clean
RUN apt-get upgrade -y && apt-get update -y
RUN apt-get install -y ffmpeg
RUN apt-get install -y ca-certificates
RUN pip install --upgrade pip
RUN pip install openai-whisper
RUN pip install "fastapi[standard]"
RUN pip install uvicorn
CMD ["python", "main.py"]