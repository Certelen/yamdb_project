FROM python:3.7-slim

WORKDIR /app

COPY ../ ./

RUN pip3 install -r api_yamdb/requirements.txt --no-cache-dir

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"] 