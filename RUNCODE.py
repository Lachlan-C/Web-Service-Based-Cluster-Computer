from time import sleep
from MPI import get_IP
from MPI import get_num_nodes
import requests
import sys

file = str(sys.argv[1])[:len(str(sys.argv[1]))-3]

for i in range(get_num_nodes()):
    url = 'http://' + get_IP(i) + ':8081/run/' + file
    print(url)
    x = requests.get(url)
