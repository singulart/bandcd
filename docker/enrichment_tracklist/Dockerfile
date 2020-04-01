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
#RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub \
#    && wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk \
#    && wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk \
#    && apk add glibc-2.30-r0.apk \
#    && apk add glibc-bin-2.30-r0.apk


#GeckoDriver
#RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz" -O /tmp/geckodriver.tgz \
#    && tar zxf /tmp/geckodriver.tgz -C /usr/bin/ \
#    && rm /tmp/geckodriver.tgz

# ChromeDriver
#RUN wget -q "https://chromedriver.storage.googleapis.com/81.0.4044.69/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
#    && unzip /tmp/chromedriver.zip -d /usr/bin/ \
#    && rm /tmp/chromedriver.zip

# libxslt.so is needed at runtime
#RUN apk add --no-cache libxslt-dev mesa-egl mesa-gles
RUN apk add --no-cache libxslt-dev
COPY --from=builder /install /usr/local
COPY storage /app/storage
COPY *.py /app/
WORKDIR /app

# Bug Chrome
#RUN mkdir /usr/lib/chromium/swiftshader/ \
#    && cp /usr/lib/libGLESv2.so.2 /usr/lib/chromium/swiftshader/libGLESv2.so \
#    && cp /usr/lib/libEGL.so.1 /usr/lib/chromium/swiftshader/libEGL.so

# Installs latest Chromium package.
#RUN echo @edge http://nl.alpinelinux.org/alpine/edge/community > /etc/apk/repositories \
#    && echo @edge http://nl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories \
#    && apk add --no-cache \
#    libstdc++@edge \
#    chromium@edge \
#    harfbuzz@edge \
#    nss@edge \
#    freetype@edge \
#    ttf-freefont@edge \
#    && rm -rf /var/cache/* \
#    && mkdir /var/cache/apk
#
# Add Chrome as a user
#RUN adduser -D chrome \
#    && chown -R chrome:chrome /app
# Run Chrome as non-privileged
#USER chrome

#ENV CHROME_BIN=/usr/bin/chromium-browser \
#    CHROME_PATH=/usr/lib/chromium/

# xvfb - X server display
#COPY xvfb-chromium /usr/bin/
#RUN ln -s /usr/bin/xvfb-chromium /usr/bin/google-chrome \
#    && chmod 777 /usr/bin/xvfb-chromium

# create symlinks to chromedriver and geckodriver (to the PATH)
#RUN ln -s /usr/bin/geckodriver /usr/bin/chromium-browser \
#    && chmod 777 /usr/bin/geckodriver \
#    && chmod 777 /usr/bin/chromium-browser

#RUN ln -s /usr/bin/geckodriver /usr/bin/chromedriver \
#    && chmod 777 /usr/bin/geckodriver \
#    && chmod 777 /usr/bin/chromedriver

# Note '-u' option: unbuffered output https://stackoverflow.com/a/29745541
ENTRYPOINT ["python3", "-u", "freeband.py"]