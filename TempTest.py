from time import sleep
import MPI
MPI.send(1,0)
sleep(1)
MPI.send(2,0)

sleep(3)
print(MPI.recieve(0))
sleep(1)
print(MPI.recieve(1))
sleep(1)
print(MPI.recieve(0))
