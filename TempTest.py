from time import sleep
import MPI
MPI.send(1,0)
MPI.send(2,0)

sleep(10)
print(MPI.recieve(1))