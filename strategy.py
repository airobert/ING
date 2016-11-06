# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com
import math # because we need to use math.inf to represet infinity
import random
import copy

epsilon = 0

class Vector(object):
	def __init__(self, k, n):
		# print ('k=', k, 'n=',n)
		self.k = k
		self.n = n
		self.numL = []
		self.bitL = []
		for i in range(n):
			v = []
			for j in range (k):
				v.append(random.randrange(0,2))
			self.bitL.append(v) 
			self.numL.append(sum(v)) 

	def getH (self, other):
		H = []
		for i in range (self.n):
			if abs(self.numL[i] - other.numL[i]) >= epsilon:
				H.append(abs(self.numL[i] - other.numL[i]))
			else:
				H.append(math.inf)
		return H

	def getG (self, other):
		G = []
		H = self.getH(other)
		mini = min(H)
		for i in range(self.n):
			if H[i] == mini:
				G.append(self.numL[i] - other.numL[i])
			else:
				G.append(0)
		return G
	
	def evolve(self):
		bitL = []
		numL = []
		# print ('s = ', self.s)
		for i in range(self.n):
			b = []
			for j in range (self.k):
				if (random.random() < 0.01): # with less than 1% of the chance to change	
					b.append((self.bitL[i][j] + 1)%2) # flip it over
					# print ('**************************')
				else:
					b.append(self.bitL[i][j])
			bitL.append(b)
			numL.append(sum(b))
		self.bitL = bitL
		self.numL = numL
		# print(' n = ', len(self.numL))

	def payoff (self, beta):
		# self = alpha
		if self.getH(beta) == math.inf:
			return 0
		else:
			sm = sum (self.getG(beta)) 
			# print (sm)
			if sm > 0:
				return 1 #POS
			elif sm == 0:
				return 0 #ZERO
			else:
				return -1 # NEG

	def __eq__(self, other): 
		return (self.numL == other.numL)


	def __str__(self):
		return str(self.numL)


	def __hash__(self):
		h = 0
		for i in range(self.n):
			h += self.numL[i] * 100
		return h

	# def mean (self):
	# 	return (sum(self.numL) / len(self.numL))

class PureStrategy(object):
	def __init__(self, k, n):
		self.vector = Vector(k, n)

	def __init__(self, vect):
		self.vector = vect


	def evolve(self):
		self.vector.evolve()
		

	def convertToMixed(self):
		return MixedStrategy([self.vector], [1.0])

	def __str__(self): # override the default printing function
		return str(self.vector)

	def __eq__(self, other): 
		return (self.vector == other.vector)

	def expectedPayoff(self, other):

		alpha = self.vector
		beta = other.vector
		return alpha.payoff(beta)

	# def mean(self):
	# 	return self.vector.mean()

		

class MixedStrategy(object):
	def __init__(self, k, n, size):
		self.d = {}
		total = 0
		for i in range(size):
			rd = random.randint(0, 5)
			v = Vector(k, n)
			# print (v)
			# print (rd)
			if v not in self.d.keys():
				self.d[v] = rd
			else: 
				self.d[v] = self.d[v] + rd 
			total += rd
		# print ('total = ',total)
		if total == 0:
			# this mixed strategy is of size one
			# strategies.append(PureStrategy(k, n).convertToMixed())
			self.d[Vector(k,n)] = 1
		else:
			for v in self.d.keys():
				self.d[v] = self.d[v]/total
		# print (sum(self.d.values()))

	def evolve (self):
		tmp = {}
		# for i in self.d.keys():
			# print (i)
		for v in self.d.keys():
			pct = self.d[v]
			w = copy.copy(v)
			w.evolve() 
			if w in tmp.keys(): 
				tmp[w] += pct 
			else:
				tmp[w] = pct
		self.d = tmp


	def support (self):
		l = []
		for v in self.d.keys(): 
			if self.d[v] != 0:
				l.append(PureStrategy(v))
		return l

	def __str__(self):# override the default printing function
		s = ''
		for v in self.d.keys():
			if self.d[v] != 0: 
				s += str(v) + ' > '+str(self.d[v])[:5] + ' |\n'
			# s += '\n'
		return s
	
	def expectedPayoff(self, other):
		payoff = 0
		for v in self.d.keys():
			pd = self.d[v]
			p = 0 
			for w in other.d.keys():
				p += v.payoff(w) * other.d[w]
			payoff += p * pd
		return payoff


	# def mean (self):
	# 	m = 0
	# 	for v in self.d.keys():
	# 		m += self.d[v] * v.mean()
	# 	return (m)


	# def median(self):
	# 	m = []
	# 	for v in self.d.keys():
	# 		m.append(v.mean())
	# 	m = sorted(m)
	# 	index = int(len(m)/2)
	# 	return (m[index])
		













	# def __eq__(self, other):
	# 	flag = True
	# 	for s in self.d.keys():
	# 		if self.d[k] != other.d[k]:
	# 			flag = False
	# 	return flag

	