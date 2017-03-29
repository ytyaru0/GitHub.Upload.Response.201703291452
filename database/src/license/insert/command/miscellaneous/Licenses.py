#!python3
#encoding:utf-8
import time
import pytz
import requests
import json
import datetime
import web.service.github.api.v3.Response
class Licenses:
    def __init__(self, data, client):
        self.data = data
        self.response = web.service.github.api.v3.Response.Response()
        self.client = client

    """
    ライセンスDBを一覧表示する。
    """
    def Show(self):
        print("{0},{1}".format('Key','Name'))
        for license in self.data.db_license['Licenses'].find(order_by=['Id']):
            print("{0},{1}".format(license['Key'],license['Name']))

    """
    指定したkeyに一致するライセンスが存在するなら、マスターDBに挿入する。
    @param {string} keyはライセンスのキー。https://developer.github.com/v3/licenses/#get-an-individual-license
    """
    def InsertOne(self, key):
        if None is not self.data.db_license['Licenses'].find_one(Key=key):
            return
        try:
            self.__InsertUpdateLicenses(self.client.license.GetLicense(key))
        except Exception as e:
            print('%r' % e)
    
    """
    ライセンスを一覧取得してマスターDBに挿入する。
    https://developer.github.com/v3/licenses/#list-all-licenses
    """
    def Update(self):
        self.data.db_license.begin()
        licenses = self.client.license.GetLicenses()
        for l in licenses:
            license = self.client.license.GetLicense(l['key'])
            self.__InsertUpdateLicenses(license)
        self.data.db_license.commit()

    def __InsertUpdateLicenses(self, j):
        record = self.data.db_license['Licenses'].find_one(Key=j['key'])
        if None is record:
            self.data.db_license['Licenses'].insert(self.__CreateRecord(j))
        else:
            self.data.db_license['Licenses'].update(self.__CreateRecord(j), ['Key'])

    def __CreateRecord(self, j):
        return dict(
            Key=j['key'],
            Name=j['name'],
            SpdxId=j['spdx_id'],
            Url=j['url'],
            HtmlUrl=j['html_url'],
            Featured=self.__BoolToInt(j['featured']),
            Description=j['description'],
            Implementation=j['implementation'],
            Permissions=self.__ArrayToString(j['permissions']),
            Conditions=self.__ArrayToString(j['conditions']),
            Limitations=self.__ArrayToString(j['limitations']),
            Body=j['body']
        )

    def __GetHttpHeaders(self):
        return {
            "Accept": "application/vnd.github.drax-preview+json",
            "Time-Zone": "Asia/Tokyo",
            "Authorization": "token {0}".format(self.data.get_access_token())
        }

    def __BoolToInt(self, bool_value):
        if True == bool_value:
            return 1
        else:
            return 0

    def __ArrayToString(self, array):
        ret = ""
        for v in array:
            ret = v + ','
        return ret[:-1]
