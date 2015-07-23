# coding: utf-8
from threading import Thread
import time
import sh
from xml.dom import minidom
import glob
import json
import traceback
import magento
import copy
from datetime import datetime
import requests
from client import *
shangpin_client = Shangpin_client()

def get_shangpin_products():
    shangpin_client.set_path('/commodity/findinfobypage')
    request_data = {"PageIndex":"1","PageSize":"100","endTime":"","startTime":""}
    shangpin_client.set_request_data(request_data)
    response = shangpin_client.req_post()
    content = response.content
    response_dict = json.loads(content, encoding="utf-8")
    if response_dict['response']['Total']>100:
        print("exceed 100 page limit!")
    else:
        pass
    return response_dict['response']['SopProductSkuIces']

def get_exactly_the_product(shangpin_productmodel, products):
    def product_filter(obj):
        pass

def sync_one_product(product):
    print(product['ProductModel'])

def start_sync():
    stock_doc = minidom.parse("./morning.inventory.hk.xml")
    erp_products = stock_doc.getElementsByTagName("product")
    shangpin_products_list = get_shangpin_products()
    print(shangpin_products_list)
    map(sync_one_product, shangpin_products_list)
    pass

start_sync()


