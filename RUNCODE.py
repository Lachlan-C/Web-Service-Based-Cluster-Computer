from time import sleep
from MPI import get_IP
from MPI import get_num_nodes
import requests

file = "MPImatrixmultiply"

for i in range(get_num_nodes()):
    url = 'http://' + get_IP(i) + ':8081/run/' + file
    print(url)
    x = requests.get(url)
