# import logging
# import logging.handlers
# from logging.handlers import WatchedFileHandler
import os
import multiprocessing

bind = "0.0.0.0:9701"  # 绑定ip和端口号
# backlog = 512  # 监听队列
# chdir = "/app/myapi"  # gunicorn要切换到的目的工作目录
# timeout = 30
# 使用gevent模式，还可以使用sync 模式，默认的是sync模式
# worker_class = "gevent"
workers = multiprocessing.cpu_count()  # 进程数
threads = 2  # 指定每个进程开启的线程数
# 设置最大并发量
worker_connections = 200
keepalive = 60  # 服务器保持连接的时间，能够避免频繁的三次握手过程
forwarded_allow_ips = "*"  # 允许哪些ip地址来访问

# 设置守护进程,将进程交给supervisor管理
# daemon = "false"

capture_output = True  # 是否捕获输出

basedir = os.path.dirname(os.path.abspath(__file__))
gun_log_dir = os.path.join(basedir, "gunicorn_log")
os.makedirs(gun_log_dir, exist_ok=True, mode=0o775)
# 设置进程文件目录
pidfile = os.path.join(gun_log_dir, "gunicorn.pid")
# 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
loglevel = "info"
# 设置访问日志和错误信息日志路径
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'  # 设置gunicorn访问日志格式，错误日志无法设置
accesslog = os.path.join(gun_log_dir, "access.log")  # 访问日志文件
errorlog = os.path.join(gun_log_dir, "error.log")  # 错误日志文件
