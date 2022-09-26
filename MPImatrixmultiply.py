from random import randint
import MPI
from time import time

# NUM = Number of Nodes

NUM = 4
number_send = int(NUM / MPI.get_num_nodes())

a = [[randint(1,99) for i in range(NUM)] for j in range(NUM)]
b = [[randint(1,99) for i in range(NUM)] for j in range(NUM)]
#a = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
#b = [[1, 3, 5, 7], [9, 8, 2, 1], [4, 14, 42, 44], [33, 45, 9, 74]]

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
        MPI.send(a[(i)*number_send:((i)*number_send)+number_send],i)
        MPI.send(b,i)

a = MPI.recieve(0)

b = MPI.recieve(0)

c = [[0]*NUM for i in range(len(a))]

for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
              c[i][j] += a[i][k] * b[k][j]

MPI.send(c,0)

if MPI.get_rank() == 0:
    output = []
    for i in range(MPI.get_num_nodes()):
        output= output+MPI.recieve(i)

    end = str(time() - start)
    f = open("OUTPUT.txt","a")
    f.write("Time: " + end + " SIZE: " + str(NUM) + "x" + str(NUM) + "\n")
    f.close()
    print("Time: ", end, " SIZE: ", str(NUM),"x",str(NUM))
