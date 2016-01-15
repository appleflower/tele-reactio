#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, join
import json
from random import choice
import datetime

class manager:
    def __init__(self):
        self.kuva = self.get_filenames("kuva")
        self.reactio = self.get_filenames("kuvaR")
        self.jew = self.get_filenames("kuvaR/jew/")
        self.cd_list = {}

        with open("settings.json","r") as f:
            try:
                self.settings = json.load(f)
            except ValueError:
                self.settings = {}
                print("Error loading settings")

        with open("cd_fail.json","r") as f:
            try:
                self.cd_fail = json.load(f)
            except ValueError:
                self.cd_fail = {}
                print("Error loading cd_fail")

    def get_filenames(self,path):
        return [f for f in listdir(path) if isfile(join(path, f))]

    def get_img(self,command):
        if command == "k":
            path = "kuva/" + choice(self.kuva)
            return open(path,"rb")
        elif command == "r":
            path = "kuvaR/" + choice(self.reactio)
            return open(path,"rb")
        elif command == "j":
            path = "kuvaR/jew/" + choice(self.jew)
            return open(path,"rb")
        else: return None

    def check_cd(self,name,delta):
        time = datetime.datetime.now()
        if time > self.cd_list[name] + datetime.timedelta(seconds=delta):
            return True
        else:
            if name not in self.cd_fail.keys():
                self.cd_fail[name] = 1
            else:
                self.cd_fail[name] += 1

            with open('cd_fail.json', 'w') as outfile:
                    json.dump(self.cd_fail, outfile)
            return False


