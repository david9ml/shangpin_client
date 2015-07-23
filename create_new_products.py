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

shangpin_client.set_path('/commodity/addsku')
request_data = {"ProductName":"Test001",
                "CategoryNo":"A03B01C02D02",
                "BrandNo":"B0562",
                "ProductModel":"mytestproduct",
                "ProductUnit": 1,
                "ProductSlogan": u"越穿越得",
                "SkuDyaAttr": 1,
                "Length": 10,
                "Width": 30,
                "Heigth": 10,
                "GrossWeight": 1,
                "ProductSex": 0,
                "MarketTime": 2015,
                "MarketSeason": u"春",
                "PackingList": u"上衣一件，扣子2枚",
                "PCDescription": u"时尚大方",
                "MobileDescription": u"时尚大方",
                "ProductAttributeDataIces": [
                    {
                        "AttibuteId": 1939,
                        "AttrValueId": 3003,
                        "TemplateId": 1364,
                        "InputAttrValue": ""
                    },
                    {
                        "AttibuteId": 1942,
                        "AttrValueId": 3005,
                        "TemplateId": 1364,
                        "InputAttrValue": ""
                    }
                ],
                "SkuInfoIces": [
                    {
                        "ProductColor": u"花花色",
                        "ColourScheme": "449",
                        "ProductSizeText": u"国际码：L",
                        "ScreenSize": "1",
                        "BarCode": "874574124514",
                        "Materials": [
                            u"棉"
                        ],
                        "PlaceOrginIds": [
                            1
                        ],
                "SkuTempValueDatas": [
                    {
                        "SizeTmpNo": "100065",
                        "SizeTmpItemId": 1,
                        "ItemValue": "17"
                    },
                    {
                        "SizeTmpNo": "100065",
                        "SizeTmpItemId": 2,
                        "ItemValue": "19"
                    }
                ]
                   }
                ]
               }
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)

