from time import sleep
import MPI

print(MPI.get_num_nodes())
MPI.send([1,2,3],0)
sleep(1)
MPI.send(2,0)

sleep(1)

MPI.get_rank()
print(type(MPI.recieve(0)))
sleep(1)
print(MPI.recieve(1))
sleep(1)
print(MPI.recieve(0))
