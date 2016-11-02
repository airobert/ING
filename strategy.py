# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com
import math # because we need to use math.inf to represet infinity
epsilon = 0.005

class Vector(object):
	l = []
	def __init__(self, lst):
		self.l = lst

	def getH (self, other):
		H = []
		if len(self.l) == len(other.l):
			for i in range (len(self.l)):
				if abs(self.l[i] - other.l[i]) >= epsilon:
					H.append(abs(self.l[i] - other.l[i]))
				else:
					H.append(math.inf)
		return H
	def getG (self, other):
		H = self.getH(other)
		mini = min(H)
		for i in range(len(self.l)):
			if H[i] == mini:
				G.append(self.l[i] - other.l[i])
			else:
				G.append(0)



class PureStrategy(object):
	def __init__(self, vector):
		self.vector = vector

	def convertToMixed(self):
		return MixedStrategy([self.vector], [1.0])

	def __str__(self): # override the default printing function
		return self.vector

	def __eq__(self, other): 
		return (self.vector == other.vector)

	def expectedPayoff(self, other):
		alpha = self.vector
		beta = other.vector
		if alpha.getH(beta) == math.inf:
			return 0
		else:
			if sum (alpha.getG(beta)) > 0:
				return 1 # POS
			else:
				return -1 # NEG



# WARNING!!!!
# I have just changed the strategy to a dictionary

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

	