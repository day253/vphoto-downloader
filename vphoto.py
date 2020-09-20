#!/usr/bin/python

from selenium import webdriver
import requests
import urllib3

urllib3.disable_warnings()

url_album = "http://api.vphotos.cn/gateway/albumphoto/v1/album/photo/mobile/find?pageSize=1000&sort=asc&lastPhotoId=&rank=3&offset=&authType=1&weChatId=EFDF6253B3B61409369354F3951BEF51&albumSn=EFDF6253B3B61409369354F3951BEF51&uId=18451005&token=f31c2c0f8717deb93170930333b6c02b"

browser = webdriver.Chrome()


class WeChat():
    def __init__(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; FRD-AL00 Build/HUAWEIFRD-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043602 Safari/537.36 MicroMessenger/6.5.16.1120 NetType/WIFI Language/zh_CN	'
        }  # 请求头信息
        self.user_list = {}
        self.session = requests.session()
        self.session.headers = headers
        self.session.verify = False

        self.photo_list = list()
        self.raw_photo_list = list()

    def get_list(self):

        response = self.session.get(url_album).json()

        for item in response:
            self.photo_list.append(item["photoId"])

        print(len(self.photo_list))

    def get_large_photo_url(self):

        url = "http://api.vphotos.cn/vphotosgallery/wechat/album/getPhotoUrl"

        for item in self.photo_list:
            data = {
                "photoId": item,
                "uid": "18451005",
                "photoSizeType": "4",
                "autoType": "1",
                "weChatId": "EFDF6253B3B61409369354F3951BEF51",
                "albumSn": "EFDF6253B3B61409369354F3951BEF51",
                "token": "f31c2c0f8717deb93170930333b6c02b",
            }

            response = self.session.post(url, data=data).json()

            print(response)

            jpg_url = response["data"]["smallUrl"]
            jpg_file = response["data"]["photoName"]

            img_file = self.session.get(jpg_url)

            with open(jpg_file, "wb") as file:
                file.write(img_file.content)

            # break


# with open("tcx.txt") as file:
#     lines = file.readlines()
#     for line in lines:
#         line = line.strip()
#         url = url_tmp % line
#         print(url)
#         browser.get(url)

wechat = WeChat()
wechat.get_list()
wechat.get_large_photo_url()

browser.quit()
