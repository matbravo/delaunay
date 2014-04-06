from triangle import *
from vertex import *
import numpy

class Delaunay:

	vertexes = []

	def __init__(self,vertexes):
		self.vertexes = vertexes
		self.triangles = []
	def analyze(self):
		pass
	def printResult(self):
		for k in range(0,len(self.vertexes),1):
			self.vertexes[k].id = k
		f = open("output.off","w")
		f.write("\tOFF\n")
		f.write(" "+str(len(self.vertexes))+" "+str(len(self.triangles))+" 0\n")
		for vertex in self.vertexes:
			f.write(str(vertex.x)+"\t"+str(vertex.y)+"\t0\n")
		for triangle in self.triangles:
			f.write("3 "+str(triangle.vertexes[0].id)+"\t"+str(triangle.vertexes[1].id)+"\t"+str(triangle.vertexes[2].id)+"\n")
	def inCircleTest(self,triangle1,triangle2):
		# Looking for the vertex not shared
		k = triangle2.neighbours.index(triangle1)
		vertex4 = triangle2.vertexes[(k+2)%3]
		vertex1 = triangle1.vertexes[0]
		vertex2 = triangle1.vertexes[1]
		vertex3 = triangle1.vertexes[2]

		M = []
		M.append([vertex1.x,vertex1.y,(vertex1.x**2)+(vertex1.y**2),1])
		M.append([vertex2.x,vertex2.y,(vertex2.x**2)+(vertex2.y**2),1])
		M.append([vertex3.x,vertex3.y,(vertex3.x**2)+(vertex3.y**2),1])
		M.append([vertex4.x,vertex4.y,(vertex4.x**2)+(vertex4.y**2),1])

		result = float(numpy.linalg.det(M))

		if result <= 0.0:
			return False
		else:
			return True



class DelaunayAnalysis1(Delaunay):

	def analyze(self):
		first_vertexes = self.getFirstBoundingRectangle()
		for vertex in self.vertexes:
			for triangle in self.triangles:
				if  self.inTriangle(vertex,triangle):
					newTriangles = self.splitTriangle(vertex,triangle)
					for newTriangle in newTriangles:
						self.legalizeTriangle(newTriangle,newTriangle.neighbours[1])
					break
		self.deleteBoundingRectangle(first_vertexes)


	def getFirstBoundingRectangle(self):
		vertexes = self.vertexes

		vertexes = sorted(vertexes, key=lambda vertex: vertex.x)
		lvertex = vertexes[0]
		rvertex = vertexes[-1]

		vertexes = sorted(vertexes, key=lambda vertex: vertex.y)
		bvertex = vertexes[0]
		tvertex = vertexes[-1]

		topleftcorner = Vertex(lvertex.x*2.0,tvertex.y*2.0)
		toprightcorner = Vertex(rvertex.x*2.0,tvertex.y*2.0)
		bottomleftcorner = Vertex(lvertex.x*2.0,bvertex.y*2.0)
		bottomrightcorner = Vertex(rvertex.x*2.0,bvertex.y*2.0)

		self.vertexes.append(topleftcorner)
		self.vertexes.append(toprightcorner)
		self.vertexes.append(bottomleftcorner)
		self.vertexes.append(bottomrightcorner)

		triangle1 = Triangle([topleftcorner,bottomleftcorner,toprightcorner],[])
		triangle2 = Triangle([bottomrightcorner,toprightcorner,bottomleftcorner],[])

		triangle1.neighbours = [EmptyTriangle(),triangle2,EmptyTriangle()]
		triangle2.neighbours = [EmptyTriangle(),triangle1,EmptyTriangle()]

		self.triangles = [triangle1,triangle2]

		return [topleftcorner,toprightcorner,bottomleftcorner,bottomrightcorner]
		
	def deleteBoundingRectangle(self,vertexes):
		for triangle in self.triangles:
			for vertex in vertexes:
				if vertex in triangle.vertexes:
					for neighbour in triangle.neighbours:
						if neighbour.__class__.__name__ != "EmptyTriangle":
							index = neighbour.neighbours.index(triangle)
							neighbour.neighbours[index] = EmptyTriangle()
					self.triangles.remove(triangle)
					break
		for vertex in vertexes:
			self.vertexes.remove(vertex)




	def inTriangle(self,vertex,triangle):
		# Cross product between vertex and point in triangle 
		for v in triangle.vertexes:
			if v == vertex :
				return False

		for k in range(0,3,1):
			vertex1 = triangle.vertexes[k]
			vertex2 = triangle.vertexes[(k+1)%3]
			if numpy.linalg.det([[vertex2.x-vertex1.x,vertex2.y-vertex1.y],[vertex.x-vertex1.x,vertex.y-vertex1.y]]) < 0.0:
				return False

		return True

	def splitTriangle(self,vertex,triangle):
		flagThree = True

		for k in range(0,3,1):
			vertex1 = triangle.vertexes[k]
			vertex2 = triangle.vertexes[(k+1)%3]
			if numpy.linalg.det([[vertex2.x-vertex1.x,vertex2.y-vertex1.y],[vertex.x-vertex1.x,vertex.y-vertex1.y]]) == 0.0:
				triangle2 = triangle.neighbours[k]
				flagThree = False
				break

		return_triangles = []

		if flagThree:
			return_triangles = self.splitInThreeTriangles(vertex,triangle)
		else:
			return_triangles = self.splitInFourTriangles(vertex,triangle,triangle2)

		return return_triangles

	def splitInFourTriangles(self,vertex,triangle1,triangle2):
		print triangle1,triangle2
		k = triangle1.neighbours.index(triangle2)
		j = triangle2.neighbours.index(triangle1)

		v1 = triangle1.vertexes
		v2 = triangle2.vertexes

		t1 = Triangle([vertex,v1[(k+1)%3],v1[(k+2)%3]],[])
		t2 = Triangle([vertex,v1[(k+2)%3],v1[k]],[])
		t3 = Triangle([vertex,v2[(j+1)%3],v2[(j+2)%3]],[])
		t4 = Triangle([vertex,v2[(j+2)%3],v2[j]],[])

		t1.neighbours = [t4,triangle1.neighbours[(k+1)%3],t2]
		t2.neighbours = [t1,triangle1.neighbours[(k+2)%3],t3]
		t3.neighbours = [t2,triangle2.neighbours[(j+1)%3],t4]
		t4.neighbours = [t3,triangle2.neighbours[(j+2)%3],t1]

		neighbours = [triangle1.neighbours[(k+1)%3],triangle1.neighbours[(k+2)%3],triangle2.neighbours[(j+1)%3],triangle2.neighbours[(j+2)%3]]
		result_triangles = [t1,t2,t3,t4]
		triangles = [triangle1,triangle1,triangle2,triangle2]

		z = 0
		for neighbour in neighbours:
			if neighbour.__class__.__name__ != "EmptyTriangle":
				index = neighbour.neighbours.index(triangles[z])
				neighbour.neighbours[index] = result_triangles[z]
			z = z+1

		self.triangles.remove(triangle1)
		self.triangles.remove(triangle2)
		self.triangles.append(t1)
		self.triangles.append(t2)
		self.triangles.append(t3)
		self.triangles.append(t4)

		return result_triangles

	def splitInThreeTriangles(self,vertex,triangle):
		vertexes = triangle.vertexes
		neighbours = triangle.neighbours

		triangle1 = Triangle([vertex,vertexes[0],vertexes[1]],[])
		triangle2 = Triangle([vertex,vertexes[1],vertexes[2]],[])
		triangle3 = Triangle([vertex,vertexes[2],vertexes[0]],[])

		#Change to new neighbours
		triangle1.neighbours = [triangle3,neighbours[0],triangle2] 
		triangle2.neighbours = [triangle1,neighbours[1],triangle3]
		triangle3.neighbours = [triangle2,neighbours[2],triangle1]

		#Change neighbours references
		result_triangles = [triangle1,triangle2,triangle3]

		k = 0
		for neighbour in neighbours:
			if neighbour.__class__.__name__ != "EmptyTriangle":
				index = neighbour.neighbours.index(triangle)
				neighbour.neighbours[index] = result_triangles[k]
			k = k+1
		
		self.triangles.append(triangle1)
		self.triangles.append(triangle2)
		self.triangles.append(triangle3)
		self.triangles.remove(triangle)

		return result_triangles

	def legalizeTriangle(self,triangle1,triangle2):
		if (triangle1.__class__.__name__ == "EmptyTriangle") or (triangle2.__class__.__name__ == "EmptyTriangle"):
			return

		t1 = triangle1
		t2 = triangle2

		# Change diagonal
		if (self.inCircleTest(t1,t2)):

			k = t1.neighbours.index(t2)
			j = t2.neighbours.index(t1)

			newTriangle1 = Triangle([t1.vertexes[(k+1)%3],t1.vertexes[(k+2)%3],t2.vertexes[(j+2)%3]],[])
			newTriangle2 = Triangle([t2.vertexes[(j+1)%3],t2.vertexes[(j+2)%3],t1.vertexes[(k+2)%3]],[])

			newTriangle1.neighbours = [t1.neighbours[(k+1)%3],newTriangle2,t2.neighbours[(j+2)%3]]
			newTriangle2.neighbours = [t2.neighbours[(j+1)%3],newTriangle1,t1.neighbours[(k+2)%3]]

			if newTriangle1.neighbours[0].__class__.__name__ != "EmptyTriangle":
				aux = newTriangle1.neighbours[0].neighbours.index(t1)
				newTriangle1.neighbours[0].neighbours[aux] = newTriangle1
			if newTriangle1.neighbours[2].__class__.__name__ != "EmptyTriangle":
				aux = newTriangle1.neighbours[2].neighbours.index(t2)
				newTriangle1.neighbours[2].neighbours[aux] = newTriangle1

			if newTriangle2.neighbours[0].__class__.__name__ != "EmptyTriangle":
				aux = newTriangle2.neighbours[0].neighbours.index(t2)
				newTriangle2.neighbours[0].neighbours[aux] = newTriangle2
			if newTriangle2.neighbours[2].__class__.__name__ != "EmptyTriangle":
				aux = newTriangle2.neighbours[2].neighbours.index(t1)
				newTriangle2.neighbours[2].neighbours[aux] = newTriangle2

			self.triangles.append(newTriangle1)
			self.triangles.append(newTriangle2)
			self.triangles.remove(t1)
			self.triangles.remove(t2)

			self.legalizeTriangle(newTriangle1,newTriangle1.neighbours[2])
			self.legalizeTriangle(newTriangle2,newTriangle2.neighbours[0])








		




