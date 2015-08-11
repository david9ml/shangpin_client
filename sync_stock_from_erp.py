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
import traceback
shangpin_client = Shangpin_client()

def get_shangpin_stock(sku_no):
    shangpin_client.set_path('/stock/findinfo')
    request_data = [sku_no]
    shangpin_client.set_request_data(request_data)
    response = shangpin_client.req_post()
    content = response.content
    '''
    print("#########################################################")
    print(request_data)
    print(content)
    print("#########################################################")
    '''
    content_dict = json.loads(content, encoding="utf-8")
    return content_dict

def update_stock(client, sku_no, qty):
    client.set_path('/stock/update')
    request_data = {"SkuNo":sku_no, "InventoryQuantity":qty }
    shangpin_client.set_request_data(request_data)
    response = shangpin_client.req_post()
    content = response.content
    print(content)

def get_shangpin_products():
    shangpin_client.set_path('/commodity/findinfobypage')
    request_data = {"PageIndex":"1","PageSize":"100","endTime":"","startTime":""}
    shangpin_client.set_request_data(request_data)
    response = shangpin_client.req_post()
    content = response.content
    response_dict = json.loads(content, encoding="utf-8")
    return_dict = response_dict['response']['SopProductSkuIces']
    if response_dict['response']['Total']>100:
        print("total:{}").format(response_dict['response']['Total'])
        print("exceed 100 page limit!")
        for i in range(2,2+response_dict['response']['Total']/100):
            request_data = {"PageIndex":str(i),"PageSize":"100","endTime":"","startTime":""}
            shangpin_client.set_request_data(request_data)
            response = shangpin_client.req_post()
            content = response.content
            response_dict = json.loads(content, encoding="utf-8")
            return_dict += response_dict['response']['SopProductSkuIces']
        return return_dict
    else:
        return return_dict

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
    shangpin_sku_no = product['SopSkuIces'][0]['SkuNo']
    #model_list = [node.getElementsByTagName("model")[0].firstChild.data for node in the_product_node_list]
    #print(the_product_node_list)
    if len(the_product_node_list) == 0 :
        print("Can't find the product in erp_products, decide to set stock zero...!!!")
        print('---' + shangpin_p_model_str + '---')
        stock_info = get_shangpin_stock(sku_no=shangpin_sku_no)
        if product['SopSkuIces'][0]['IsDeleted'] == 1:
            print("product deleted in shangpin...skip...")
            pass
        else:
            if stock_info['response'][0]['InventoryQuantity'] == 0:
                print("shangpin stock already zero...skip...")
            else:
                update_stock(shangpin_client, shangpin_sku_no, 0)
                print("set stock zero complete!!!")

    elif len(the_product_node_list) == 1 :
        if product['SopSkuIces'][0]['SkuStatus'] == 2:
            stock_info = get_shangpin_stock(sku_no=shangpin_sku_no)
            print("We find the exact product, update stock !")
            erp_qty = the_product_node_list[0].getElementsByTagName("quatity")[0].firstChild.data
            shangpin_qty = stock_info['response'][0]['InventoryQuantity']
            if int(erp_qty) == int(shangpin_qty):
                print("already equal: erp_qty=shangpin_qty...skip...")
            else:
                update_stock(shangpin_client, shangpin_sku_no, erp_qty)
                print("not equal update %s;%s;%s complete!!!" % (str(shangpin_sku_no), str(shangpin_qty), str(erp_qty)))
        else:
            print("product not in sale...skip...")
            pass
    else:
        print("What's wrong buddy?")
    time.sleep(1)

def start_sync():
    stock_doc = minidom.parse("./morning.inventory.hk.xml")
    erp_products = stock_doc.getElementsByTagName("product")
    shangpin_products_list = get_shangpin_products()
    print(shangpin_products_list)
    print(len(shangpin_products_list))
    map(functools.partial(sync_one_product, erp_products=erp_products), shangpin_products_list)
    pass

while True:
    start_sync()
    import gc
    gc.collect()
    print("sleep 5*60 sec...")
    time.sleep(5*60)

