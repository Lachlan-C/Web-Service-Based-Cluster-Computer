import random
import math
import MPI
from time import time

NITER = 10000000

NUM = NITER / MPI.get_num_nodes()

start = time()
count = 0
for i in range(int(NUM)):
    x = random.random()
    y = random.random()
    if x**2 +y**2 <= 1:
        count += 1
pi = 4*float(count)/NUM

MPI.send(pi,0)

if MPI.get_rank() == 0:
    output=0

    for i in range(MPI.get_num_nodes()):
        output += MPI.recieve(i)
    output = output / MPI.get_num_nodes()

    end = str(time() - start)
    f = open("OUTPUT-PI.txt","a")
    f.write("Time: " + end + " NITTER: " + str(NITER) + "\n")
    f.close()
    print("Time: ", end, " PI: ", str(output))
