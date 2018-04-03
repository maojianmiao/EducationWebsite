#coding:utf-8

import os
import subprocess
import glob


def replace(s):
    result = []

    cmd = r'dir *.py /S /b'
    print cmd

    folders = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print folders

    for i in folders.split():
        with open(i.strip(),'rb') as f:
            data = f.read()
            data = data.replace(s,'linyuling')
        with open(i.strip(),'wb') as f:
            f.write(data)
        
        print('{} is finished'.format(i))


if __name__=='__main__':
    s = 'linyuling'
    replace(s)
