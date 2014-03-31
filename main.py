import sys
import os
from triangle import *
from vertex import *
from delaunay import *


triangles = []
vertexes = []





def main(argv):
	f = open(argv[0],"r")
	for line in f:
		splitedLine = line.split()
		vertex = Vertex(splitedLine[0],splitedLine[1])
		vertexes.append(vertex)

if __name__=='__main__':
	main(sys.argv[1:])