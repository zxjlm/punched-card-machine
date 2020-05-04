# -*- coding:utf-8 -*-
__author__ = 'harumonia'

import re
import urllib
import datetime


def clean_data(s):
    data_today = datetime.date.today().__str__().replace('-', '/')

    url = re.search('curl \'(https://.+?)\' -H', s).group(1)
    head_list = re.findall('-H \'(.*?)\'', s)
    headers = {re.match('(.*?): (.*)', foo).group(1): re.match('(.*?): (.*)', foo).group(2) for foo in head_list}
    cook = headers.pop('Cookie')
    cookies = {foo1.split('=')[0]: foo1.split('=')[1] for foo1 in cook.split(';')}
    data_raw = re.search('.* --data \'(.+?)\'', s).group(1)
    data = {foo1.split('=')[0]: urllib.parse.unquote(foo1.split('=')[1]) for foo1 in data_raw.split('&')}
    data['DATETIME_CYCLE'] = data_today
    return url, headers, cookies, data


def get_name(s):
    data_raw = re.search('.* --data \'(.+?)\'', s).group(1)
    data = {foo1.split('=')[0]: urllib.parse.unquote(foo1.split('=')[1]) for foo1 in data_raw.split('&')}
    for k, v in data.items():
        if k.startswith('XM'):
            return v

