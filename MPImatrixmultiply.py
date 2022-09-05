from random import randint
import MPI
from time import time

# Hardcoded NUM = Nodes

NUM = 8
number_send = int(NUM / MPI.get_num_nodes())

a = [[randint(1,99) for i in range(NUM)] for j in range(NUM)]
b = [[randint(1,99) for i in range(NUM)] for j in range(NUM)]
c = [[0]*NUM for i in range(NUM)]

start = time()

if MPI.get_rank() == 0:

    start = time()
    # SENDING TO ALL BUT MAIN
    #count = MPI.get_num_nodes() - 1
    #for i in range(count-1):
        #MPI.send(a,i + 1)
        #MPI.send(b[(i+1)*number_send:((i+1)*number_send)+number_send],i + 1)
    
    # SENDING TO ALL
    count = MPI.get_num_nodes()
    for i in range(count):
        MPI.send(a,i)
        MPI.send(b[(i)*number_send:((i)*number_send)+number_send],i)

a = MPI.recieve(0)
b = MPI.recieve(0)

for i in range(len(b)): 
        for j in range(len(a[0])):
            for k in range(len(a)):
              c[i][j] += b[i][k] * a[k][j]

MPI.send(c,0)

if MPI.get_rank() == 0:
    output = []
    for i in range(MPI.get_num_nodes()):
        output.append(MPI.recieve(i))
    print(time() - start)