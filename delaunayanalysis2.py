from delaunay import *
import numpy

class DelaunayAnalysis2(Delaunay):

	def analyze(self):
		first_vertexes = self.getFirstBoundingRectangle()
		for vertex in self.vertexes:
			for triangle in self.triangles:
				if  self.inTriangle(vertex,triangle):
					newTriangles = self.splitTriangle(vertex,triangle)
					for newTriangle in newTriangles:
						self.legalizeTriangle(newTriangle,newTriangle.neighbours[1])
					break

		for edge in self.edges:
			self.constraintEdge(edge)

		self.deleteBoundingRectangle(first_vertexes)

	def constraintEdge(self,edge):
		v1 = self.vertexes[edge[0]]
		v2 = self.vertexes[edge[1]]

		self.createPath(v1,v2)

	def createPath(self,vertexSrc,vertexDest):

		#if vertexSrc in triangleSrc.vertexes and vertexDest in triangleSrc.vertexes:
		#	return
		midVector = [float(vertexDest.x-vertexSrc.x) , float(vertexDest.y-vertexSrc.y)]
		midVertex = Vertex(float(vertexSrc.x+midVector[0]/2.0,),float(vertexSrc.y+midVector[1]/2.0))

		self.vertexes.append(midVertex)

		for triangle in self.triangles:
			if self.inTriangle(midVertex,triangle):
				newTriangles = self.splitTriangle(midVertex,triangle)
				break

		tSrc = Triangle()
		tDest = Triangle()

		for triangle in newTriangles:
			v1 = midVertex
			v2 = triangle.vertexes[1]
			v3 = triangle.vertexes[2]
			if numpy.linalg.det([[v2.x-v1.x,v2.y-v1.y],[vertexDest.x-v1.x,vertexDest.y-v1.y]]) >= 0.0 and numpy.linalg.det([[vertexDest.x-v1.x,vertexDest.y-v1.y],[v3.x-v1.x,v3.y-v1.y]]) >= 0.0:
				tDest = triangle
			elif numpy.linalg.det([[v2.x-v1.x,v2.y-v1.y],[vertexSrc.x-v1.x,vertexSrc.y-v1.y]]) >= 0.0 and numpy.linalg.det([[vertexSrc.x-v1.x,vertexSrc.y-v1.y],[v3.x-v1.x,v3.y-v1.y]]) >= 0.0:
				tSrc = triangle

		newTrianglesSrc = self.legalizeTriangle(tSrc,tSrc.neighbours[1])
		newTrianglesDest = self.legalizeTriangle(tDest,tDest.neighbours[1])

		if not (vertexSrc in newTrianglesSrc[0].vertexes or vertexSrc in newTrianglesSrc[1].vertexes) :
			self.createPath(midVertex,vertexSrc)

		if not (vertexDest in newTrianglesDest[0].vertexes or vertexDest in newTrianglesDest[1].vertexes):
			self.createPath(midVertex,vertexDest)

	def lookForTriangleToCreatePath(self,vertexSrc,vertexDest,triangle):
		v1 = vertexSrc

		triangle_aux = triangle

		while True:
			k = triangle_aux.vertexes.index(v1)
			v2 = triangle_aux.vertexes[(k+1)%3]
			v3 = triangle_aux.vertexes[(k+2)%3]

			if numpy.linalg.det([[v2.x-v1.x,v2.y-v1.y],[vertexDest.x-v1.x,vertexDest.y-v1.y]]) >= 0.0:
				if numpy.linalg.det([[vertexDest.x-v1.x,vertexDest.y-v1.y],[v3.x-v1.x,v3.y-v1.y]]) >= 0.0:
					return triangle_aux
				else:
					triangle_aux = triangle_aux.neighbours[(k+2)%3]
			else:
				triangle_aux = triangle_aux.neighbours[k]










