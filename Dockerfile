
FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
		  python3.9\
		  python3-pip\
		  libglib2.0-0\
          libnss3\
          libnspr4\
          libatk1.0-0\
          libatk-bridge2.0-0\
          libcups2\
          libdbus-1-3\
          libxcb1\
          libdrm2\
          libxkbcommon0\
          libx11-6\
          libxcomposite1\
          libxdamage1\
          libxext6\
          libxfixes3\
          libxrandr2\
          libgbm1\
          libgtk-3-0\
          libpango-1.0-0\
          libcairo2\
          libgdk-pixbuf2.0-0\
          libasound2\
          libatspi2.0-0 \
		  libxshmfence1 \
		  libegl1 \
		  curl \
		  python3-venv

#RUN apt-get install dumb-init

WORKDIR /rssinn

COPY ./requirements.txt ./requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple

RUN playwright install

RUN playwright install chromium

COPY . /rssinn

ENTRYPOINT ["dumb-init", "--"]

EXPOSE 8085

RUN chmod +x start.sh
ENTRYPOINT ["./start.sh"]
