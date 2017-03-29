#!python3
#encoding:utf-8
import os.path
import urllib.parse
import subprocess
import dataset
class Data:
    def __init__(self, path_dir_pj, path_dir_db, user_name, description, homepage):
        self.user_name = user_name
        self.description = description
        self.homepage = homepage
        self.path_dir_pj = path_dir_pj
        self.path_dir_db = path_dir_db
        self.path_db_account = os.path.join(self.path_dir_db, 'GitHub.Accounts.sqlite3')
        self.path_db_repo = os.path.join(self.path_dir_db, 'GitHub.Repositories.{0}.sqlite3'.format(self.user_name))
        self.path_db_license = os.path.join(self.path_dir_db, 'GitHub.Licenses.sqlite3')
        self.path_db_api = os.path.join(self.path_dir_db, 'GitHub.Apis.sqlite3')
        self.path_db_lang = os.path.join(self.path_dir_db, 'GitHub.Languages.sqlite3')
        self.path_db_other_repo = os.path.join(self.path_dir_db, 'GitHub.Repositories.__other__.sqlite3')
        self.path_db_gnu_license = os.path.join(self.path_dir_db, 'GNU.Licenses.sqlite3')
        self.db_account = None
        self.db_repo = None
        self.db_license = None
        self.db_api = None
        self.db_lang = None
        self.db_other_repo = None
        self.db_gnu_license = None
        self.load_db()
    def load_db(self):
        if None is self.db_account and os.path.isfile(self.path_db_account):
            self.db_account = dataset.connect('sqlite:///' + self.path_db_account)
        if None is self.db_repo and os.path.isfile(self.path_db_repo):
            self.db_repo = dataset.connect('sqlite:///' + self.path_db_repo)
        if None is self.db_license and os.path.isfile(self.path_db_license):
            self.db_license = dataset.connect('sqlite:///' + self.path_db_license)
        if None is self.db_api and os.path.isfile(self.path_db_api):
            self.db_api = dataset.connect('sqlite:///' + self.path_db_api)
        if None is self.db_lang and os.path.isfile(self.path_db_lang):
            self.db_lang = dataset.connect('sqlite:///' + self.path_db_lang)
        if None is self.db_other_repo and os.path.isfile(self.path_db_other_repo):
            self.db_other_repo = dataset.connect('sqlite:///' + self.path_db_other_repo)
        if None is self.db_gnu_license and os.path.isfile(self.path_db_gnu_license):
            self.db_gnu_license = dataset.connect('sqlite:///' + self.path_db_gnu_license)
    def get_username(self):
        return self.user_name
    def set_username(self, username):
        if None is not self.db_account['Accounts'].find_one(Username=username):
            self.user_name = username
    def get_ssh_host(self):
        return "github.com.{0}".format(self.user_name)
    def get_mail_address(self):
        return self.db_account['Accounts'].find_one(Username=self.get_username())['MailAddress']
    def get_access_token(self, scopes=None):
        sql = "SELECT * FROM AccessTokens WHERE AccountId == {0}".format(self.db_account['Accounts'].find_one(Username=self.get_username())['Id'])
        if not(None is scopes):
            sql = sql + " AND ("
            for s in scopes:
                sql = sql + "(',' || Scopes || ',') LIKE '%,{0},%'".format(s) + " OR "
            sql = sql.rstrip(" OR ")
            sql = sql + ')'
        return self.db_account.query(sql).next()['AccessToken']
    def get_repo_name(self):
        return os.path.basename(self.path_dir_pj)        
    def get_repo_description(self):
        return self.description
    def get_repo_homepage(self):
        return self.homepage

# ----------------------------------------------- database/src/other_repo/insert,repo
    def get_other_username(self, urlstring):
        return self.__url_to_names(urlstring)[0]
    def get_other_repo_name(self, urlstring):
        return self.__url_to_names(urlstring)[1]
    def __url_to_names(self, urlstring, is_show=False):
        url = urllib.parse.urlparse(urlstring)
        if is_show:
            print(urlstring)
            print(url.path)
            print(os.path.split(url.path))
            print(os.path.split(url.path[1:]))
            print(self.get_split_pass(url.path[1:]))
        return self.get_split_pass(url.path[1:])
    """
    パスを配列に分解する。
    今回はurllib.parse.urlparse().pathの部分の1番目=user, 2番目=リポジトリ名として取得したい。
    os.path.split()は末尾要素とそれ以前のすべての２つにしか分解されないため使えない。
    https://docs.python.jp/3/library/os.path.html#os.path.split
    パス区切り文字はos.nameで区別する。
    https://docs.python.jp/3/library/os.html#os.name
    """
    def get_split_pass(self, urlstring):
        # Windows('nt')
        if 'nt' == os.name:
            return urlstring.split('\\')
        # Linux,Mac('posix'), Android('java')
        else:
            return urlstring.split('/')
# -----------------------------------------------
