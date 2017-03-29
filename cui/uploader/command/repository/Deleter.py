#!python3
#encoding:utf-8
import os
import subprocess
import shlex
import shutil
import time
import pytz
import requests
import json
import datetime

class Deleter:
    def __init__(self, data, client):
        self.data = data
        self.client = client

    def ShowDeleteRecords(self):
        repo = self.data.db_repo['Repositories'].find_one(Name=self.data.get_repo_name())
        print(repo)
        print(self.data.db_repo['Counts'].find_one(RepositoryId=repo['Id']))
        for record in self.data.db_repo['Languages'].find(RepositoryId=repo['Id']):
            print(record)

    def Delete(self):
        self.__DeleteLocalRepository()
        self.client.repo.delete()
        self.__DeleteDb()

    def __DeleteLocalRepository(self):
        shutil.rmtree('.git')

    def __DeleteDb(self):
        repo = self.data.db_repo['Repositories'].find_one(Name=self.data.get_repo_name())
        self.data.db_repo.begin()
        self.data.db_repo['Repositories'].delete(Id=repo['Id'])
        self.data.db_repo['Counts'].delete(RepositoryId=repo['Id'])
        self.data.db_repo['Languages'].delete(RepositoryId=repo['Id'])
        self.data.db_repo.commit()

