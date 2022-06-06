FROM python:3-alpine
COPY requirements.txt requirements.txt
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps
COPY netflix_api.py netflix_api.py
COPY .env .env
CMD uvicorn netflix_api:app --host 0.0.0.0 --port $PORT