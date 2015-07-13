# -*- coding: utf-8 -*-
from secret_file import *
from time import gmtime, strftime
import requests
import json
import hashlib

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
        self.timestamp = strftime("%Y-%M-%d %H:%M")
        self.data = {'app_key': self.app_key, 'timestamp': self.timestamp}
        md5_sign = "app_key=" + self.app_key + "&timestamp=" + self.timestamp + "_" + self.app_secret
        m = hashlib.md5()
        m.update(md5_sign)
        self.sign = m.hexdigest()
        self.data['sign'] = self.sign

    def set_data(self):
        pass

    def req_post(self):
        print("params:")
        print(self.params)
        print("data:")
        print(self.data)
        #response = requests.post(self.url+self.path, params = self.params, data=json.dumps(self.data), headers=self.headers)
        response = requests.post(self.url+self.path, params = self.params, data=self.data, headers=self.headers)
        print(response.content)

    def set_path(self, path_value):
        self.path = path_value
