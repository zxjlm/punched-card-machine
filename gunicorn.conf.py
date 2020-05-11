# -*- coding:utf-8 -*-
__author__ = 'harumonia'


# import os
# import gevent.monkey
# gevent.monkey.patch_all()

# import multiprocessing

# debug = True
# threads = 2
# worker_connections = 200
loglevel = 'info'
bind = "0.0.0.0:5000"
pidfile = '/logs/gunicorn/gunicorn.pid'
accesslog = '/logs/gunicorn/gunicorn_acess.log'
errorlog = '/logs/gunicorn/gunicorn_error.log'
# docker 下不能启动这个
# daemon = True

# 启动的进程数
# workers = multiprocessing.cpu_count()
workers = 1
worker_class = 'sync'
# x_forwarded_for_header = 'X-FORWARDED-FOR'


# # gunicorn.conf

# # 并行工作进程数
# workers = 2
# # 指定每个工作者的线程数
# threads = 2
# # 监听内网端口5000
# bind = '0.0.0.0:5000'
# # 设置守护进程,将进程交给supervisor管理
# daemon = 'true'
# # 工作模式协程
# # worker_class = 'gevent'
# # 设置最大并发量
# worker_connections = 2000
# # 设置进程文件目录
# pidfile = '/logs/gunicorn/gunicorn.pid'
# # 设置访问日志和错误信息日志路径
# accesslog = '/logs/gunicorn/gunicorn_acess.log'
# errorlog = '/logs/gunicorn/gunicorn_error.log'
# # 设置日志记录水平
# loglevel = 'info'
