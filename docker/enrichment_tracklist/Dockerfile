FROM python:3.6-alpine as base

FROM base as builder
RUN apk add --no-cache --virtual /.build-deps gcc libc-dev libxslt-dev libxml2 libxml2-dev
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt
RUN apk del /.build-deps

FROM base

# Otherwise geckodriver wasn't working, see https://stackoverflow.com/a/58771365
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub \
    && wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk \
    && wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk \
    && apk add glibc-2.30-r0.apk \
    && apk add glibc-bin-2.30-r0.apk

#GeckoDriver
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz" -O /tmp/geckodriver.tgz \
    && tar zxf /tmp/geckodriver.tgz -C /usr/bin/ \
    && rm /tmp/geckodriver.tgz \
    && chmod 755 /usr/bin/geckodriver

# libxslt.so is needed at runtime
RUN apk add libxslt-dev xvfb firefox-esr
COPY --from=builder /install /usr/local
COPY storage /app/storage
COPY *.py /app/
WORKDIR /app

# xvfb - X server display
COPY xvfb-ffox /usr/bin/
RUN chmod 777 /usr/bin/xvfb-ffox

ENTRYPOINT ["/usr/bin/xvfb-ffox"]