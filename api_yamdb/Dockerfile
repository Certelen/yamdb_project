FROM python:3.7-slim

WORKDIR /app

COPY ../ ./

RUN pip3 install -r api_yamdb/requirements.txt --no-cache-dir

ENV PYTHONPATH api_yamdb

CMD ["gunicorn", "--bind", "0:8000", "api_yamdb.wsgi:application"]
