import os
import time
from datetime import datetime, timedelta

usersDir = []

os.chdir('music')

def checkExpirationTime():
    while True:
        dir_path = os.listdir()
        for i in dir_path:
            if i not in usersDir:
                usersDir.append(i)
        print(usersDir)
        removeDirs = []
        for user in usersDir:
            with open(f'{user}/expiration', 'r') as exp_file:
                exp_time = exp_file.read()
                exp_time = datetime.strptime(exp_time,"%m/%d/%Y %H:%M:%S")
                time_delta = exp_time + timedelta(seconds=60)
                if datetime.now() > time_delta:
                    removeDirs.append(user)
                else:
                    exp_file.close()
        removeExpirationDir(removeDirs)
        removeDirs.clear()
        print('qweqweqwe')
        time.sleep(60)

def removeExpirationDir(removeDirs):
    for dir in removeDirs:
        usersDir.remove(dir)
        dir_path = os.listdir(str(dir))
        for i in dir_path:
            os.remove(f'{dir}/' + i)
        os.rmdir(str(dir))

checkExpirationTime()