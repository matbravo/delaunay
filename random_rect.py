import random

f = open("input.txt","w")

r = float(100.0*random.random())


for k in range(0,300,1):
	x = float(r*2*random.random()-r)
	y = float(r*2*random.random()-r)
	f.write(str(x)+" "+str(y)+"\n")

