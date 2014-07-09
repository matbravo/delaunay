import random
import sys


def randomN(N):
	f = open("input.txt","w")
	r = float(100.0*random.random())
	f.write(str(N)+" 0\n")

	for k in range(0,N,1):
		x = float(r*2*random.random()-r)
		y = float(r*2*random.random()-r)
		f.write(str(x)+" "+str(y)+"\n")

def randomEdges(N):
	f = open("input.txt","w")
	r = float(100.0*random.random())
	f.write(str(N)+" 12\n")

	aux = r/6.0
	f.write("0.0 "+str(aux)+"\n")
	f.write(str(-2.0*aux)+" "+str(2.0*aux)+"\n")
	f.write(str(-2.0*aux)+" "+str(aux)+"\n")
	f.write(str(-2.0*aux)+" "+str(-2.0*aux)+"\n")
	f.write(str(-1.0*aux)+" "+str(-2.0*aux)+"\n")
	f.write(str(-1.0*aux)+" "+str(aux)+"\n")
	f.write("0.0 0.0\n")
	f.write(str(aux)+" "+str(aux)+"\n")
	f.write(str(aux)+" "+str(-2.0*aux)+"\n")
	f.write(str(2.0*aux)+" "+str(-2.0*aux)+"\n")
	f.write(str(2.0*aux)+" "+str(aux)+"\n")
	f.write(str(2.0*aux)+" "+str(2.0*aux)+"\n")

	for k in range(0,N-12,1):
		x = float(r*2*random.random()-r)
		y = float(r*2*random.random()-r)
		f.write(str(x)+" "+str(y)+"\n")

	for k in range(0,12,1):
		f.write(str(k)+" "+str((k+1)%12)+"\n")


def main(argv):

	method = int(argv[0])

	N = int(argv[1])	

	if method == 1:
		randomN(N)
	elif method == 2:
		randomEdges(N)	
	


if __name__=='__main__':
	main(sys.argv[1:])