# This is a simple Dockerfile to use while developing
# It's not suitable for production
#
# It allows you to run both flask and celery if you enabled it
# for flask: docker run --env-file=.flaskenv image flask run
# for celery: docker run --env-file=.flaskenv image celery worker -A myapi.celery_app:app
#
# note that celery will require a running broker and result backend

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
