#!/usr/bin/python3
#!python3
#encoding:utf-8
import sys
import os.path
import subprocess
import configparser
import argparse
import database.src.Create
import cui.uploader.Main

class Main:
    def __init__(self):
        pass

    def Run(self):
        parser = argparse.ArgumentParser(
            description='GitHub Repository Uploader.',
        )
        parser.add_argument('path_dir_pj')
        parser.add_argument('-u', '--username')
        parser.add_argument('-d', '--description')
        parser.add_argument('-l', '--homepage', '--link', '--url')
        args = parser.parse_args()
        print(args)
        print('path_dir_pj: {0}'.format(args.path_dir_pj))
        print('-u: {0}'.format(args.username))
        print('-d: {0}'.format(args.description))
        print('-l: {0}'.format(args.homepage))

        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))
        path_dir_db = os.path.abspath(config['Path']['DB'])
        print(path_dir_db)
        
        if None is args.username:
            args.username = config['GitHub']['User']
            print('default-username: {0}'.format(args.username))
        print(os.path.join(path_dir_db, 'GitHub.Accounts.sqlite3'))
        print(os.path.join(path_dir_db, 'GitHub.Repositories.{0}.sqlite3'.format(args.username)))
        
        data = database.src.Data.Data(args.path_dir_pj, path_dir_db, args.username, args.description, args.homepage)
        
        creator = database.src.Create.InitializeMasterDbCreator(data)
        data = creator.Run()

        main = cui.uploader.Main.Main(data)
        main.Run()


if __name__ == '__main__':
    main = Main()
    main.Run()
