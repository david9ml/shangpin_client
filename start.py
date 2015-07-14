from client import *
import time

shangpin_client = Shangpin_client()
'''
while True:
    shangpin_client.set_path('/commodity/findinfobypage')
    request_data = {"PageIndex":"1","PageSize":"100","endTime":"","startTime":""}
    shangpin_client.set_request_data(request_data)
    shangpin_client.req_post()
    shangpin_client.reset()
    time.sleep(1)
'''
shangpin_client.set_path('/commodity/findinfobypage')
request_data = {"PageIndex":"1","PageSize":"100","endTime":"","startTime":""}
shangpin_client.set_request_data(request_data)
shangpin_client.req_post()


