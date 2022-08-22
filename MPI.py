import string
import requests
import sys
import socket

def get_IP(rank):
    with open('servers.txt') as f:
        content = f.readlines()
    return content[rank].replace("\n", "")

def get_rank():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('1.1.1.1', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    print('CURRENT IP: ' + IP)
    with open('servers.txt') as f:
        content = f.readlines()
    index = [x for x in range(len(content)) if IP in content[x].lower()]
    return index[0]

def send(data, destRank):
    url = 'http://' + get_IP(destRank) + ':8080/recv'

    dest = get_IP(destRank)

    myobj = {'data':data,'dest':dest}

    x = requests.post(url, json=myobj)

    print(x.text)

def recieve(source):
    string
    url = 'http://' + str(get_IP(get_rank())) + ':8080/recv' #+ str(source) 
    print(url)
    return requests.get(url)