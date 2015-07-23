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
import functools
from client import *
shangpin_client = Shangpin_client()

def get_shangpin_stock(sku_no):
    shangpin_client.set_path('/stock/findinfo')
    request_data = [sku_no]
    shangpin_client.set_request_data(request_data)
    response = shangpin_client.req_post()
    content = response.content
    print("#########################################################")
    print(request_data)
    print(content)
    print("#########################################################")

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

def get_exactly_the_product(shangpin_p_model_list, erp_products):
    def product_filter(node, shangpin_p_model_list_lenth):
        try:
            model_str = node.getElementsByTagName("model")[0].firstChild.data
        except:
            model_str = ""
        try:
            material_str = node.getElementsByTagName("material")[0].firstChild.data
        except:
            material_str = ""
        try:
            color_str = node.getElementsByTagName("color")[0].firstChild.data
        except:
            color_str = ""
        if shangpin_p_model_list_lenth == 1:
            if shangpin_p_model_list[0] == model_str:
                return True
            else:
                return False
        elif shangpin_p_model_list_lenth == 2:
            if (shangpin_p_model_list[0] == model_str and shangpin_p_model_list[1] == material_str) or (shangpin_p_model_list[0] == model_str and shangpin_p_model_list[1] == color_str):
                return True
            else:
                return False
        elif shangpin_p_model_list_lenth == 3:
            if shangpin_p_model_list[0] == model_str and shangpin_p_model_list[1] == material_str and shangpin_p_model_list[2] == color_str:
                return True
            else:
                return False
    filtered_list = filter(functools.partial(product_filter, shangpin_p_model_list_lenth = len(shangpin_p_model_list)), erp_products)
    return filtered_list

def sync_one_product(product, erp_products):
    shangpin_p_model_str = product['ProductModel']
    shangpin_p_model_list = shangpin_p_model_str.split()
    the_product_node_list = get_exactly_the_product(shangpin_p_model_list=shangpin_p_model_list, erp_products=erp_products)
    #model_list = [node.getElementsByTagName("model")[0].firstChild.data for node in the_product_node_list]
    #print(the_product_node_list)
    if len(the_product_node_list) == 0 :
        print("Can't find the product in erp_products, decide to ignore or set stock zero...")
    elif len(the_product_node_list) == 1 :
        print("We find the exact product, update stock !")
        sku_no = product['SopSkuIces'][0]['SkuNo']
        get_shangpin_stock(sku_no=sku_no)
    else:
        print("What's wrong buddy?")

def start_sync():
    stock_doc = minidom.parse("./morning.inventory.hk.xml")
    erp_products = stock_doc.getElementsByTagName("product")
    shangpin_products_list = get_shangpin_products()
    print(shangpin_products_list)
    map(functools.partial(sync_one_product, erp_products=erp_products), shangpin_products_list)
    pass

start_sync()


