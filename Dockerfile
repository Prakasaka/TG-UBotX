# We're using Alpine Edge
FROM python:3.7-alpine


# Installing Packages
RUN apk add --no-cache --update \
    bash \
    build-base \
    bzip2-dev \
    curl \
    coreutils \
    gcc \
    g++ \
    git \
    util-linux \
    libevent \
    libjpeg-turbo-dev \
    jpeg-dev \
    jpeg \
    libc-dev \
    libffi-dev \
    libpq \
    libwebp-dev \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    musl-dev \
    openssl-dev \
    postgresql \
    postgresql-client \
    postgresql-dev \
    openssl \
    pv \
    jq \
    wget \
    python \
    python-dev \
    python3 \
    python3-dev \
    readline-dev \
    ffmpeg \
    sqlite-dev \
    sudo \
    zlib-dev \
    zip
    

#
# Clone repo and prepare working directory
#
RUN git clone 'https://github.com/Prakasaka/TG-UBotX.git' /root/userbot
RUN mkdir /root/userbot/bin/
WORKDIR /root/userbot/

#
# Copies session and config (if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* /root/userbot/

#
# Install requirements
#
RUN pip install -r requirements.txt
RUN pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U
CMD ["python3","-m","userbot"]
