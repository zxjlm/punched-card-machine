FROM python:3.7
WORKDIR /Project/daily_reporter
COPY . .
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
RUN mkdir -p /logs/gunicorn/


CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]