# -*- coding: utf-8 -*-
from secret_file import *
from time import gmtime, strftime
import requests
import json
import hashlib
import urllib

class Shangpin_client(object):
    def __init__(self):
        self.app_key = APP_KEY
        self.app_secret = APP_SECRET
        self.params = {}
        self.data = {}
        self.url = 'http://111.204.231.201:9090'
        self.timestamp = ''
        self.sign = ''
        self.path = ''
        self.headers = {'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'}
        self.init_data()

    def print_secrets(self):
        print(self.app_key)
        print(self.app_secret)

    def print_time(self):
        #print(strftime("%d %Y %H:%M:%S +0000"))
        print(strftime("%Y-%M-%d %H:%M"))

    def init_data(self):
        self.timestamp = strftime("%Y-%m-%d %H:%M")
        self.data = {'app_key': self.app_key.encode("utf-8"), 'timestamp': self.timestamp.encode("utf-8")}

    def set_sign(self):
        md5_sign = "app_key=" + urllib.quote_plus(self.app_key.encode("utf-8")) + "&request=" + urllib.quote_plus(self.data['request'])+ "&timestamp=" + urllib.quote_plus(self.timestamp.encode('utf-8')) + "_" + self.app_secret.encode('utf-8')
        #md5_sign = "app_key=" + urllib.quote_plus(self.app_key.encode("utf-8")) + "&request=" + self.data['request'] + "&timestamp=" + urllib.quote_plus(self.timestamp.encode('utf-8')) + "_" + self.app_secret.encode('utf-8')
        print("md5_sign")
        print(md5_sign)
        #md5_sign = "app_key=" + self.app_key + "&request=" + self.data['request']+ "&timestamp=" + self.timestamp + "_" + self.app_secret
        #print(md5_sign)
        m = hashlib.md5()
        m.update(md5_sign)
        self.sign = m.hexdigest()
        self.data['sign'] = self.sign.upper()

    def set_data(self):
        pass

    def req_post(self):
        request_val = {"PageIndex":"1","PageSize":"100","endTime":"","startTime":""}
        print(json.dumps(request_val))
        self.data['request'] = json.dumps(request_val, sort_keys=True, ensure_ascii=False).encode('utf8')
        #self.data['request'] = urllib.quote_plus(json.dumps(request_val, sort_keys=True))
        self.set_sign()
        print("data:")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(self.data)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #response = requests.post(self.url+self.path, data=urllib.urlencode(self.data), headers=self.headers)
        response = requests.request('POST', self.url+self.path, data=self.data, headers=self.headers)
        print(response.content)

    def set_path(self, path_value):
        self.path = path_value
