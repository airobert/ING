# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com
import math # because we need to use math.inf to represet infinity
import random


class Vector(object):
	bitL = []
	numL = []
	def __init__(self, k, n):
		for i in range(n):
			v = []
			for j in range (k):
				v.append(random.randrange(0,2))
			self.bitL.append(v) 
			self.numL.append(sum(v))

	def getH (self, other):
		H = []
		for i in range (len(self.numL)):
			if abs(self.numL[i] - other.numL[i]) >= epsilon:
				H.append(abs(self.numL[i] - other.numL[i]))
			else:
				H.append(math.inf)
		return H

	def getG (self, other):
		G = []
		H = self.getH(other)
		mini = min(H)
		for i in range(len(self.numL)):
			if H[i] == mini:
				G.append(self.numL[i] - other.numL[i])
			else:
				G.append(0)
		return G

	def evlove(self):
		bitL = []
		numL = []
		for i in range(n):
			b = []
			n = []
			for j in range (k):
				if (random.random() < 0.01): # with less than 1% of the chance to change	
					b.append((self.bitL[i][j] + 1)%2) # flip it over
					# n.append(sum(self.bitL[i]))
				else:
					b.append(self.bitL[i])
					# n.append(self.numL[i])
				n.append(sum(self.bitL[i]))
			bitL.append(b)
			numL.append(n)
		self.bitL = bitL
		self.numL = numL



	def __str__(self):
		return str(self.bitL) + '\n' + str(self.numL)



class PureStrategy(object):
	def __init__(self, k, n):
		self.vector = Vector(k, n)
		

	def convertToMixed(self):
		return MixedStrategy([self.vector], [1.0])

	def __str__(self): # override the default printing function
		return str(self.vector)

	def __eq__(self, other): 
		return (self.vector == other.vector)

	def expectedPayoff(self, other):
		alpha = self.vector
		beta = other.vector
		if alpha.getH(beta) == math.inf:
			return 0
		else:
			sm = sum (alpha.getG(beta)) 
			print (sm)
			if sm > 0:
				return 1 #POS
			elif sm == 0:
				return 0 #ZERO
			else:
				return -1 # NEG


class MixedStrategy(object):
	d = {}
	def __init__(self, vectors, probabilities):
		if len(vectors) == len(probabilities) and 1 - sum(probabilities) < 0.0001 :
			for i in range (len(vectors)):
				self.d[vectors[i]] = probabilities[i]
		else:
			print ('error', vectors, probabilities, sum(probabilities)) # TODO: make this an exception
		
	def support (self):
		l = []
		for k in self.d.keys():
			if self.d[k] != 0:
				l.append(PureStrategy(k))
		return l

	def __str__(self):# override the default printing function
		s = ''
		for i in self.d.keys():
			if self.d[i] != 0:
				s += str(i) + ' > '+str(self.d[i]) + ' | '
		return s

	def __eq__(self, other):
		flag = True
		for k in self.d.keys():
			if self.d[k] != other.d[k]:
				flag = False
		return flag

	