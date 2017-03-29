#!python3
#encoding:utf-8
import web.service.github.api.v3.Response
import web.service.github.api.v3.RequestParam
from web.service.github.api.v3.miscellaneous import Licenses
from web.service.github.api.v3.repositories import Repositories
class Client(object):
    def __init__(self, data):
        self.__data = data
        self.__reqp = web.service.github.api.v3.RequestParam.RequestParam(self.__data)
        self.__response = web.service.github.api.v3.Response.Response()
        self.license = Licenses.Licenses(self.__data, self.__reqp, self.__response)
        self.repo = Repositories.Repositories(self.__data, self.__reqp, self.__response)
