FROM python:3.7
COPY . /Project
WORKDIR /Project
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
RUN mkdir -p /logs/gunicorn/
EXPOSE 5008
VOLUME "/var/logs"
CMD ["gunicorn", "app:app", "-c", "gunicorn.conf.py"]