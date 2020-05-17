from flask import Flask, request, render_template, flash
from flask_apscheduler import APScheduler
import datetime
import requests
import redis
from secure import redis_host, redis_port, redis_password
# from telegram_info import TelegramHandler
from utils import clean_data, get_name

app = Flask(__name__)
app.secret_key = 'zxjjjsama'

r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

scheduler = APScheduler(app=app)
scheduler.start()


# tele = TelegramHandler(r)
# tele.start_query()


@scheduler.task(trigger='cron', id='test_job', hour='*')
def test_job():
    hour = datetime.datetime.now().hour
    for foo in r.hvals(hour):
        url, headers, cookies, data = clean_data(foo)
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        name = get_name(foo)
        if response.json()['result']:
            r.hset('success', datetime.datetime.now().__str__()[:13].replace(' ', '-'), name)

        else:
            r.hset('fail', datetime.datetime.now().__str__()[:13].replace(' ', '-'), name)
        # print(data['XM_407868'], response.json()['result'])


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        form = request.form
        if form['curl'].startswith('curl') and '|' not in form['curl']:
            name = get_name(form['curl'])
            r.hset(form['time'], name, form['curl'])
            flash('add success', 'success')
            app.logger.info('{} record success'.format(name))
        else:
            flash('别乱输东西好吧= =', 'danger')

    dic = {foo: ','.join(list(r.hgetall(foo).keys())) for foo in range(0, 24) if
           ','.join(list(r.hgetall(foo).keys())) != ''}
    return render_template('index.html', success_log=r.hgetall('success'), fail_log=r.hgetall('fail'), info=dic)


@app.route('/logging')
def log_test():
    app.logger.info('{} record success'.format(r.get('hello')))
    return 'success'


if __name__ == '__main__':
    app.run()
