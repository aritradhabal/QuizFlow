FROM python:3.13

ENV PYTHONUNBUFFERED=true

WORKDIR /QuizFlow

COPY requirements.txt ./


RUN apt-get update && \
    apt-get install -y python3-all-dev portaudio19-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY .streamlit /root/.streamlit
COPY . .

RUN python -c "import whisper; whisper.load_model('base')" && \
    mv /root/.cache/whisper/base.pt . && \
    rm -rf /root/.cache

EXPOSE 8080
CMD ["streamlit", "run", "--server.port=8080", "--server.enableCORS=false", "Welcome.py"]
