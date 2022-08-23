import string
import requests
import sys
import socket
from time import sleep

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
    with open('servers.txt') as f:
        content = f.readlines()
    index = [x for x in range(len(content)) if IP in content[x].lower()]
    return index[0]

def send(data, destRank):
    url = 'http://' + get_IP(destRank) + ':8080/recv'

    sender = get_rank()

    myobj = {'data':data,'from':sender}

    x = requests.post(url, json=myobj)

def recieve(source):
    
    while True:
        url = 'http://' + str(get_IP(get_rank())) + ':8080/recv/' + str(source)
        message = requests.get(url).text
        if message != "ARRAY EMPTY":
            break
        sleep(1)
    return message