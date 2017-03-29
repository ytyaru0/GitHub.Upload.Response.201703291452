#!python3
#encoding:utf-8
import subprocess
import shlex
import shutil
import os.path
import getpass
import dataset
import database.src.Data
import database.src.language.insert.Main
import database.src.gnu_license.create.Main
import database.src.gnu_license.insert.main
import database.src.license.insert.Main
import database.src.other_repo.insert.Main
import database.src.account.Main
import database.src.api.Main
import database.src.repo.insert.Main
class InitializeMasterDbCreator:
    def __init__(self, data, client):
        self.data = data
        self.path_dir_this = os.path.abspath(os.path.dirname(__file__))
        self.db_files = [
            {'FileName': 'GitHub.Languages.sqlite3', 'Creator': self.__CreateLanguages, 'Inserter': self.__InsertLanguages},
            {'FileName': 'GitHub.Apis.sqlite3', 'Creator': self.__CreateApis, 'Inserter': self.__InsertApis},
            {'FileName': 'GNU.Licenses.sqlite3', 'Creator': self.__CreateGnuLicenses, 'Inserter': self.__InsertGnuLicenses},

            {'FileName': 'GitHub.Accounts.sqlite3', 'Creator': self.__CreateAccounts, 'Inserter': self.__InsertAccounts},
            {'FileName': 'GitHub.Licenses.sqlite3', 'Creator': self.__CreateLicenses, 'Inserter': self.__InsertLicenses},
            {'FileName': 'GitHub.Repositories.__other__.sqlite3', 'Creator': self.__CreateOtherRepo, 'Inserter': self.__InsertOtherRepo},
            {'FileName': 'GitHub.Repositories.{user}.sqlite3', 'Creator': self.__CreateRepo, 'Inserter': self.__InsertRepo},
        ]
        self.client = client

    def Run(self):
        if not(os.path.isdir(self.data.path_dir_db)):
            print('DBディレクトリを作る----------------')
            os.mkdir(self.data.path_dir_db)
        for db in self.db_files:
            db_path = os.path.join(self.data.path_dir_db, db['FileName'])
            if 'GitHub.Repositories.{user}.sqlite3' == db['FileName']:
                self.__LoopAccounts(db, db_path)
            else:
                if not(os.path.isfile(db_path)):
                    print('DBファイルを作る: {0} ----------------'.format(db_path))
                    db['Creator'](db_path)
                    self.data.load_db()
                    db['Inserter'](db_path)
        return self.data

    def __LoopAccounts(self, db, db_path):
        if not(os.path.isfile(db_path)):
            db['Creator'](db_path)
            self.data.load_db()
        default_user = self.data.get_username()
        try:
            for account in self.data.db_account['Accounts'].find():
                print(account['Username'])
                db_path_new = db_path.replace("{user}", account['Username'])
                if not(os.path.isfile(db_path_new)):
                    shutil.copyfile(db_path, db_path_new)
                    self.data.set_username(account['Username'])
                    print('{0}のリポジトリDBに挿入します------------------------------'.format(self.data.get_username()))
                    print(db_path_new)
                    self.data.db_repo = dataset.connect('sqlite:///' + db_path_new)
                    db['Inserter'](db_path_new)
        finally:
            self.data.set_username(default_user)
            if None is not default_user or 0 < len(default_user.strip()):
                self.data.db_repo = dataset.connect('sqlite:///' + os.path.join(self.data.path_dir_db, 'GitHub.Repositories.{0}.sqlite3'.format(self.data.get_username())))
                print('デフォルトユーザのリポジトリ接続>>>>>>>>>>>>>>>>>>>>>>>>>')
        
    def __CreateApis(self, db_path):
        a = database.src.api.Main.Main(db_path)
        a.Run()

    def __InsertApis(self, db_path):
        pass

    def __CreateRepo(self, db_path):
        path_sh = os.path.join(self.path_dir_this, 'repo/create/Create.sh')
        subprocess.call(shlex.split("bash \"{0}\" \"{1}\"".format(path_sh, db_path)))

    def __InsertRepo(self, db_path):
        m = database.src.repo.insert.Main.Main(self.data, self.client)
        m.Initialize()

    def __CreateAccounts(self, db_path):
        a = database.src.account.Main.Main(db_path)
        a.Run()

    def __InsertAccounts(self, db_path):
        pass

    def __CreateOtherRepo(self, db_path):
        path_sh = os.path.join(self.path_dir_this, 'other_repo/create/Create.sh')
        subprocess.call(shlex.split("bash \"{0}\" \"{1}\"".format(path_sh, db_path)))

    def __InsertOtherRepo(self, db_path):
        path_db_license = os.path.join(self.data.path_dir_db, "GitHub.Licenses.sqlite3")
        print(path_db_license)
        main = database.src.other_repo.insert.Main.Main(self.data, self.client)
        main.Initialize()

    def __CreateLanguages(self, db_path):
        path_sh = os.path.join(self.path_dir_this, 'language/create/Create.sh')
        subprocess.call(shlex.split("bash \"{0}\" \"{1}\"".format(path_sh, db_path)))

    def __InsertLanguages(self, db_path):
        creator_language = database.src.language.insert.Main.Main(self.data, self.client)
        creator_language.Run()

    def __CreateGnuLicenses(self, db_path):
        creator_language = database.src.gnu_license.create.Main.Main(db_path)
        creator_language.Run()

    def __InsertGnuLicenses(self, db_path):
        creator_gnu_license = database.src.gnu_license.insert.main.GnuSite(db_path)
        creator_gnu_license.GetAll()

    def __CreateLicenses(self, db_path):
        path_sh = os.path.join(self.path_dir_this, 'license/create/Create.sh')
        subprocess.call(shlex.split("bash \"{0}\" \"{1}\"".format(path_sh, db_path)))

    def __InsertLicenses(self, db_path):
        creator_license = database.src.license.insert.Main.Main(self.data, self.client)
        creator_license.Initialize()

