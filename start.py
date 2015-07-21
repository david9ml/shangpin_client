# -*- coding: utf-8 -*-
from client import *
import time
import json

shangpin_client = Shangpin_client()
# 3.2 商品批量分页查询(loop)
while True:
    shangpin_client.set_path('/commodity/findinfobypage')
    request_data = {"PageIndex":"1","PageSize":"100","endTime":"","startTime":""}
    shangpin_client.set_request_data(request_data)
    shangpin_client.req_post()
    response = shangpin_client.req_post()
    content = response.content
    print(content)
    shangpin_client.reset()
    time.sleep(1)
'''
# 3.2 商品批量分页查询(loop)
shangpin_client.set_path('/commodity/findinfobypage')
request_data = {"PageIndex":"1","PageSize":"100","endTime":"","startTime":""}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
'''
'''
# 1.1. 供货价查询
shangpin_client.set_path('/supply/findinfo')
request_data = {"Starttime":"","Endtime":"", "SkuNos":"30003221001", "PriceStatus":""}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
'''
'''
# 1.2. 供货价更新 未完成
shangpin_client.set_path('/supply/updateprice')
request_data = {"SkuNo":"30003221001","SupplyPrice":"100.00","MarkePrice":"900.00"}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
'''
'''
# 2.1 库存查询
shangpin_client.set_path('/stock/findinfo')
request_data = ["30003221001", "30002856001"]
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
'''
'''
# 2.1 库存更新
shangpin_client.set_path('/stock/update')
request_data = {"SkuNo":"30003221001", "InventoryQuantity":100 }
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
'''
'''
shangpin_client.set_path('/purchase/findporderbypage')
request_data = {"PageIndex":"1","PageSize":"100","UpdateTimeBegin":"","UpdateTimeEnd":""}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
'''

#response_dict = json.loads(content)
#print(response_dict.keys())
#print(response_dict['response'].keys())



