FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD uvicorn bot:app --host 0.0.0.0 --port ${PORT:-7876}
