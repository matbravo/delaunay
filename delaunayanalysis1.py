from delaunay import *

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