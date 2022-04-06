
FROM python:3.8-buster

RUN apt-get update

RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget

RUN apt-get install dumb-init

WORKDIR /rssinn

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /rssinn

ENTRYPOINT ["dumb-init", "--"]

#CMD ["gunicorn", "run:app", "-w", "2", "-k","uvicorn.workers.UvicornH11Worker", "-b", "0.0.0.0:28085", "--timeout", "600", "--keep-alive", "0"]

#https://blog.csdn.net/qq_25310669/article/details/120535803
CMD ["daphne", "run:app", "-b", "0.0.0.0", "-p", "28085"]

#CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "28085"]
