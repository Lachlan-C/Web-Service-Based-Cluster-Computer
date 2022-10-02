from re import M
from time import sleep
from MPI import get_IP
from MPI import get_num_nodes
import requests
import sys

file = str(sys.argv[1])

for i in range(get_num_nodes()):
    url = 'http://' + get_IP(i) + ':8081/upload/' + file

    myobj = bytearray()

    f = open(file,"rb")

    myobj = f.read()

    print(myobj)

    f.close()

    x = requests.post(url, myobj)
