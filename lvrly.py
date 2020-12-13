#! /usr/bin/env python3
#coding:utf-8
#
#
#
#
import time
import csv
import subprocess
import netifaces
import urllib.request

url = "https://hoge.hoge.org/insert_lvrly.php" 
hwa = netifaces.ifaddresses('eth0')[netifaces.AF_PACKET][0]['addr']

target = {}
presult = {}
cnt = {}

with open('/usr/local/etc/lvrly.ini',newline='') as csvf:
    lvr = csv.reader(csvf,delimiter=',')
    for row in lvr:
        if (row[0]=="QRA"):
            thisis = row[1]
        elif (row[0]=="QSY"):
            url = row[1]
        else:
            target[row[0]] = row[1]
#            print("IP={0}  HOSTNAME={1}".format(row[0],row[1]))

while True:
    for k in target:
        try:
            c = cnt[k]
        except:
            cnt[k] = 0
        a=subprocess.run(["fping","-q","-r 1","-t 100",k])
#        print("K={0}  V={1}   R={2}".format(k,target[k],a.returncode))
        try:
            z = presult[k]
        except KeyError:
            presult[k] = 0
        if presult[k]!=a.returncode:
            params = {
                "T":"C",
                "M":hwa.replace(':',''),
                "A":thisis,
                "K":k,
                "V":target[k],
                "C":a.returncode
            }
            presult[k] = a.returncode
            c = urllib.parse.urlencode(params)
#            print(c)
            req = urllib.request.Request('{}?{}'.format(url,c))
            with urllib.request.urlopen(req) as res:
                body = res.read()
#                print(body)
        cnt[k] = cnt[k] + 1
        if cnt[k]>60:
            cnt[k] = 0
            params = {
                "T":"R",
                "M":hwa.replace(':',''),
                "A":thisis,
                "K":k,
                "V":target[k],
                "C":a.returncode
            }
            c = urllib.parse.urlencode(params)
#           print(c)
            req = urllib.request.Request('{}?{}'.format(url,c))
            with urllib.request.urlopen(req) as res:
                body = res.read()
#                print(body)
    time.sleep(1)

