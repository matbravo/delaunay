import sys
import os
from triangle import *
from vertex import *
from delaunay import *
from delaunayanalysis2 import *
from delaunayanalysis1 import *



def main(argv):
	f = open(argv[0],"r")

	# Header N vertex E edges
	# v1_x v1_y
	# v2_x v2_y
	# ...
	# vN_x vN_y
	# e1_v1 e1_v2
	# e2_v1 e2_v2
	# ...
	# eE_v1 eE_v2
	aux = f.readline()
	aux = aux.split()
	N = int(aux[0])
	E = int(aux[1])

	triangles = []
	vertexes = []
	edges = []

	for k in range(0,N,1):
		line = (f.readline()).split()
		vertex = Vertex(float(line[0]),float(line[1]))
		vertexes.append(vertex)

	for k in range(0,E,1):
		line = (f.readline()).split()
		edge = []
		edge.append(int(line[0]))
		edge.append(int(line[1]))
		edges.append(edge)


	#for line in f:
	#	splitedLine = line.split()
	#	vertex = Vertex(float(splitedLine[0]),float(splitedLine[1]))
	#	vertexes.append(vertex)

	if argv[1] == "1":
		delaunay = DelaunayAnalysis1(vertexes,edges)
	elif argv[1] == "2":
		delaunay = DelaunayAnalysis2(vertexes,edges)

	delaunay.analyze()
	delaunay.printResult()

if __name__=='__main__':
	main(sys.argv[1:])