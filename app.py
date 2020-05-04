import redis
from flask import Flask, request, render_template, jsonify, flash
from flask_apscheduler import APScheduler
import datetime
import requests

from utils import clean_data, get_name

app = Flask(__name__)
app.secret_key = 'zxjjjsama'
scheduler = APScheduler(app=app)
scheduler.start()
r = redis.Redis(host='121.36.94.97', port=6379, decode_responses=True)


@scheduler.task(trigger='cron', id='test_job', hour='*')
def test_job():
    hour = datetime.datetime.now().hour
    for foo in r.hvals(hour):
        url, headers, cookies, data = clean_data(foo)
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        if response.json()['result']:
            r.hset('success', datetime.datetime.now().__str__()[:13].replace(' ', '-'), data['XM_407868'])
        else:
            r.hset('fail', datetime.datetime.now().__str__()[:13].replace(' ', '-'), data['XM_407868'])
        print(data['XM_407868'], response.json()['result'])


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        form = request.form
        name = get_name(form['curl'])
        r.hset(form['time'], name, form['curl'])
        flash('add success', 'success')
    return render_template('index.html', success_log=r.hgetall('success'), fail_log=r.hgetall('fail'))


@app.route('/redis_test')
def redis_test():
    r.set('name', '张鑫剑111')  # 设置 name 对应的值
    return 'succ'


if __name__ == '__main__':
    app.run()
