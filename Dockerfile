FROM python:3.10-slim
#RUN useradd westhide
#USER westhide
RUN mkdir /app
WORKDIR /app

COPY requirements.txt  ./
RUN pip install -U pip -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com && \
    pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

COPY myapi ./
COPY gunicorn.conf.py ./

CMD gunicorn -c gunicorn.conf.py myapi.wsgi:app
EXPOSE 9701
