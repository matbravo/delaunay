import sys
import os
from triangle import *
from vertex import *
from delaunay import *


triangles = []
vertexes = []


def main(argv):
	f = open(argv[0],"r")
	k = 0
	for line in f:
		splitedLine = line.split()
		vertex = Vertex(float(splitedLine[0]),float(splitedLine[1]))
		vertexes.append(vertex)
	delaunay = DelaunayAnalysis1(vertexes)
	delaunay.analyze()
	delaunay.printResult()

if __name__=='__main__':
	main(sys.argv[1:])