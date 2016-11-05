# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

import random

from pulp import *
from strategy import *
import sys



class Agent: # the default one is a Naive agent playing simple a strategy
	# payoff  function
	def __init__ (self, k, n, sigma):
		self.k = k
		self.n = n
		# at the beginning N is inialised as an arbitrary pure strategy
		self.piN = random.choice(self.pureStrategies).convertToMixed()
		self.N = self.piN.support() 
		# M is initialised as empty list
		self.M = []
			
	# every time the searching heuristic returns to the most num strategies.
	# if after termi_num, there is no new winning strategy discovered, we terminate 
	def iteration (self, num, termi_num):

		# 0) initialize meory and update with a random stategy

		# 1) initialize population of szie 100 with random stategies

		# 2) evolve population aginst N for 30 generations (one poch)
			# a) evaluate each individual (pure strategy) s in the population aginst N
			# b) the fitness of individual i is fi
			# c) copy the 10 most-fit individuals to the next generateion
			# d) fill the remaining 90 positions with offspring using fitness proportinate

		# 3) If highest-scoring individual ^s in population beats N, then update memory with s^

		# 4) go to step 1.

	def solve(self, WNM):
		# WNM is a list of pure strategies
		# create a matrix
		size = len(WNM)
		M = []
		for i in WNM:
			# print ('row:', i)
			r = [] # a row
			for j in WNM:
				# print ('\tcolumn', j)
				r.append(self.payoff(i, j))
			M.append(r)
		# print (M)

		# TODO : Robert needs to document these
		prob = LpProblem("solve", LpMaximize) # the row player is always trying to maximise

		# define size-many variables
		variables = []
		for w in WNM:
			x = LpVariable('y'+str(w.value), 0, 1)
			variables.append(x)

		v = LpVariable("v", 0)

		# Objective
		prob += v

		# Constraints
		for row in M:
			acc = 0
			for i in range(size):
				acc += row[i] * variables[i]
			prob += v <= acc # the column player will always want to minimise

		acc = 0
		for x in variables:
			acc += x
		prob += acc == 1


		GLPK().solve(prob)
		print ('------------------solving-------------------------')
		# Solution
		values = []
		probabilities = []
		for v in prob.variables():
			for w in WNM:
				if v.name == 'y'+ str(w.value) and v.varValue != 0:
					values.append(w.value)
					probabilities.append(v.varValue)
		print ("objective=", value(prob.objective))

		self.piN = MixedStrategy(values, probabilities)




	def searchWithHeuristic(self, num):
		strategies = []
		for n in range(num):
			# obtain a mixed strategy of random size
			size = random.randrange(1, len(self.pureStrategies)+1) # any number between 1 and len(self.pureStragegies)
			# print('size',size)
			# st = [] # the pure strategy 
			pc = {} # the percentage
			#initialise the dictionary
			for v in self.pureStrategies:
				pc[v.value] = 0

			total = 0
			for i in range(size):
				c = random.choice(self.pureStrategies).value
				rd = random.randint(0, 5)
				pc[c] = pc[c] + rd 
				total += rd
				# print ('total',total)
				# print ('keys ', pc.keys(), ' values ', pc.values(), 'total', total)

			if total == 0:
				# this mixed strategy is of size one
				strategies.append(random.choice(self.pureStrategies).convertToMixed())
			else:
				for v in self.pureStrategies:
					i = v.value
					pc[i] = pc[i]/total
					# print ('so', i, pc[i])
				strategies.append(MixedStrategy(list(pc.keys()), list(pc.values())))

		return strategies




	def play(self):
		return self.piN