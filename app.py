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
            r.hset('success', name, datetime.datetime.now().__str__()[:13].replace(' ', '-'))
            app.logger.info(
                '{}-{} report success'.format(datetime.datetime.now().__str__()[:13].replace(' ', '-'), name))

        else:
            r.hset('fail', name, datetime.datetime.now().__str__()[:13].replace(' ', '-'))
            app.logger.info('{}-{} report fail'.format(datetime.datetime.now().__str__()[:13].replace(' ', '-'), name))
        # print(data['XM_407868'], response.json()['result'])


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        form = request.form
        try:
            if '.sh' in form['curl'] or 'formDesignApi/S/' not in form['curl']:
                flash('注入攻击?不存在的~', 'danger')
            elif form['curl'].startswith('curl') and '|' not in form['curl']:
                curl = form['curl'].replace('--data-raw', '--data')
                name = get_name(curl)
                r.hset(form['time'], name, curl)
                flash('add success', 'success')
                app.logger.info('{} record success'.format(name))
            else:
                flash('别乱输东西好吧= =', 'danger')
        except Exception as e:
            flash('凉凉,建议联系管理员,{}'.format(e), 'danger')

    dic = {foo: ','.join(list(r.hgetall(foo).keys())) for foo in range(0, 24) if
           ','.join(list(r.hgetall(foo).keys())) != ''}
    return render_template('index.html', success_log=r.hgetall('success'), fail_log=r.hgetall('fail'), info=dic)


@app.route('/logging')
def log_test():
    app.logger.info('{} record success'.format(r.get('hello')))
    return 'success'


if __name__ == '__main__':
    app.run()
