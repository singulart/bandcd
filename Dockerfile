FROM python:3.6-alpine as base

FROM base as builder
RUN apk add --no-cache --virtual /.build-deps gcc libc-dev libxslt-dev libxml2 libxml2-dev
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt
RUN apk del /.build-deps

FROM base
COPY --from=builder /install /usr/local
COPY storage /app/storage
COPY *.py /app/
WORKDIR /app
ENTRYPOINT ["python3", "releases_meta.py"]