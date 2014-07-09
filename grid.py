import os

maxx = 40
maxy = 20
delta = 1

f = open("input.txt","w")

for x in range(-maxx,maxx,1):
	for y in range(-maxy,maxy,1):
		f.write(str(x)+" "+str(y)+"\n")
