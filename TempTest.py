from re import M
from time import sleep
from MPI import get_IP
import requests

file = "test"

url = 'http://' + get_IP(0) + ':8081/upload/' + file

myobj = bytearray()

f = open(file + ".py","rb")

myobj = f.read()

print(myobj)

f.close()

x = requests.post(url, myobj)