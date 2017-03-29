#!python3
#encoding:utf-8
import json
import time
from urllib.parse import urlparse
import re
class Response:
    def __init__(self):
        self.re_content_type_raw = re.compile('application/vnd.github.*.raw')
        self.re_charset = re.compile(r'charset=', re.IGNORECASE)
        self.__mime_type = None
        self.__char_set = None
    def Get(self, r, sleep_time=2, is_show=True):
#    def Get(self, r, res_type=None, success_code=None, sleep_time=2, is_show=True):
        if is_show:
            print("HTTP Status Code: {0}".format(r.status_code))
            print(r.text)
        time.sleep(sleep_time)
        r.raise_for_status()
#        if None is not success_code:
#            if (success_code != r.status_code):
#                raise Exception('HTTP Error: {0}'.format(r.status_code))
#                return None
        
        self.__SplitContentType(r)
        if None is self.__mime_type:
            return r.text
        elif 'application/json' == self.__mime_type:
            return r.json()
        elif self.re_content_type_raw.match(self.__mime_type):
            return r.content
        else:
            raise Exception('対象外のContent-Typeです。: ' + self.__mime_type)
        """
        if not('Content-Type' in r.headers) or (None is r.headers['Content-Type']) or ('' == r.headers['Content-Type']):
            return r.text
        elif 'application/json' == r.headers['Content-Type']:
            return r.json()
        elif self.re_content_type_raw.match(r.headers['Content-Type']):
            return r.content
        else:
            raise Exception('対象外のContent-Typeです。: ' + r.headers['Content-Type'])        
        """
#        if None is res_type or 'text' == res_type.lower():
#            return r.text
#        elif 'json' == res_type.lower():
#            return r.json()
#        elif 'binary' == res_type.lower():
#            return r.content
#        else:
#            raise Exception("指定されたres_type {0} は対象外です。".format(res_type))

    def __SplitContentType(self, r):
        if not('Content-Type' in r.headers) or (None is r.headers['Content-Type']) or ('' == r.headers['Content-Type']):
            self.__mime_type = None
            self.__char_set = None
        else:
            self.__mime_type, self.__char_set = r.headers['Content-Type'].split(';')
            if None is not self.__mime_type:
                self.__mime_type = self.__mime_type.strip()
            if None is not self.__char_set:
                # 'charset='を大小文字に関わらず削除する
                self.__char_set = re.sub(self.re_charset, '', self.__char_set).strip()
#                self.__char_set = self.__char_set.strip()
#                if re.compile(self.__char_set, re.IGNORECASE).match('charset=') != None:
#                self.__char_set = self.__char_set.replace('charset=', '')
#                self.__char_set = self.__char_set.replace('Charset=', '')
#                self.__char_set = self.__char_set.replace('CharSet=', '')
#                self.__char_set = self.__char_set.replace('CHARSET=', '')
        print('MimeType: {0}'.format(self.__mime_type))
        print('CharSet: {0}'.format(self.__char_set))
        
    def __SplitCharSet(self, content_type):
        self.__char_set = None


    def GetLink(self, r, rel='next'):
        if None is r.links:
            return None
        if 'next' == rel or 'prev' == rel or 'first' == rel or 'last' == rel:
            return r.links[rel]['url']
    def GetLinkNext(self, r):
        return self.__get_page(r, 'next')
    def GetLinkPrev(self, r):
        return self.__get_page(r, 'prev')
    def GetLinkFirst(self, r):
        return self.__get_page(r, 'first')
    def GetLinkLast(self, r):
        return self.__get_page(r, 'last')
    def __get_page(self, r, rel='next'):
        if None is r:
            return None
        print(r.links)
        if rel in r.links.keys():
            url = urlparse(r.links[rel]['url'])
            print('page=' + url.query['page'])
            return url.query['page']
        else:
            return None
