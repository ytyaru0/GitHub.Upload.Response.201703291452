#!python3
#encoding:utf-8
import os
import time
import pytz
import requests
import json
import datetime

class Editor:
    def __init__(self, data, client):
        self.data = data
        self.client = client

    def Edit(self, name, description, homepage):
        j = self.client.repo.edit(name, description, homepage)
        self.__EditDb(j)
        # リポジトリ名の変更が成功したら、ディレクトリ名も変更する
        if self.data.get_repo_name() != name:
            os.rename("../" + self.data.get_repo_name(), "../" + name)

    def __EditDb(self, j):
        repo = self.data.db_repo['Repositories'].find_one(Name=self.data.get_repo_name())
        data = {}
        data['Id'] = repo['Id']
        data['Name'] = j['name']
        if not(None is j['description'] or '' == j['description']):
            data['Description'] = j['description']
        if not(None is j['homepage'] or '' == j['homepage']):
            data['Homepage'] = j['homepage']
        data['CreatedAt']=j['created_at']
        data['PushedAt']=j['pushed_at']
        data['UpdatedAt']=j['updated_at']
        data['CheckedAt']="{0:%Y-%m-%dT%H:%M:%SZ}".format(datetime.datetime.now(pytz.utc))
        self.data.db_repo['Repositories'].update(data, ['Id'])
