#!python3
#encoding:utf-8
import time
import pytz
import requests
import json
import datetime
class Licenses:
    def __init__(self, data, reqp, response):
        self.data = data
        self.reqp = reqp
        self.response = response

    """
    全ライセンス情報を取得する。
    使用してみると一部ライセンスしか取得できない。CC0は取得できなかった。
    @return {array} ライセンス情報
    """
    def GetLicenses(self):
        licenses = []
        url = 'https://api.github.com/licenses'
        while (None is not url):
            r = requests.get(url, headers=self.__GetHttpHeaders())
            licenses += self.response.Get(r)
            url = self.response.GetLinkNext(r)
        return licenses

    """
    指定したライセンスの情報を取得する。
    @param  {string} keyはGitHubにおけるライセンスを指定するキー。
    @return {dict}   結果(JSON)
    """
    def GetLicense(self, key):
        url = 'https://api.github.com/licenses/' + key
        r = requests.get(url, headers=self.__GetHttpHeaders())
        return self.response.Get(r)

    """
    リポジトリのライセンスを取得する。
    @param  {string} usernameはユーザ名
    @param  {string} repo_nameは対象リポジトリ名
    @return {dict}   結果(JSON形式)
    """
    def GetRepositoryLicense(self, username, repo_name):
        url = 'https://api.github.com/repos/{0}/{1}'.format(username, repo_name)
        r = requests.get(url, headers=self.__GetHttpHeaders())
        return self.response.Get(r)

    def __GetHttpHeaders(self):
        headers = {
            "Time-Zone": "Asia/Tokyo",
            "Authorization": "token {0}".format(self.data.get_access_token()),
            "Accept": "application/vnd.github.v3+json",
        }
        headers["Accept"] = "application/vnd.github.drax-preview+json"
        return headers
        # GitHub.Apis.sqlite3にまだ`/licenses`が登録されていない
        # いちいちDB問い合わせが生じるため面倒。固定値を返したほうが早い。
#        return self.reqp.get('GET', '/licenses')

