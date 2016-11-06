# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

import random

from pulp import *
from strategy import *
import sys



class Agent: # the default one is a Naive agent playing simple a strategy
	# payoff  function
	def __init__ (self, k, n, epsilon):
		self.k = k
		self.n = n
		self.epsilon = epsilon
		# at the beginning N is inialised as an arbitrary pure strategy
		# self.piN = random.choice(self.pureStrategies).convertToMixed()
		self.size = 4 # I am not sure about this. Is this going to be important @Frans?
		self.piN = MixedStrategy(self.k, self.n, self.size) 
		self.N = self.piN.support() 
		# M is initialised as empty list
		self.M = []
			
	# every time the searching heuristic returns to the most num strategies.
	# if after termi_num, there is no new winning strategy discovered, we terminate 
	def iteration (self, termi_num):
		# 0) initialize meory and update with a random stategy
		self.piN = MixedStrategy(self.k, self.n, self.size) # starting from a random mixed strategy of size 3
		
		print('piN = ', self.piN)
		print ('===================================================')
		Hundred = 100
		# 1) initialize population of size 100 with random stategies
		population = [] 
		# print ('initial population')
		for i in range (Hundred):
			# add to the population
			population.append(MixedStrategy(self.k, self.n, self.size))
			print (i, ' is \n', population[i] , '\n') 

		termi = 0 
		epoch = 0
		mean = []
		median = []
		while (termi < termi_num):
			print ('\n\n\n\n\n\nterminate?', termi)
			# 2) evolve population against N for 30 generations (one poch)
			# best = 0
			for it in range (30):
				# print ('****************\n\nthis is iteration \n\n', it)
				# a) evaluate each individual (pure strategy) s in the population aginst N
				w = []
				for i in range(Hundred):
					p = population[i]
					w.append(p.expectedPayoff(self.piN))

				# print ('after evaluation, w is', w)


				# b) the fitness of individual i is fi
				w_min = min(w)
				f = []
				for i in range (Hundred):
					f.append(w[i] - w_min + 0.1) # why this ?

				# print ('\n\n\nafter evaluation, f is', f)

				# c) copy the 10 most-fit individuals to the next generateion
				ten_best = []# the index of the ten best
				
				for i in range (10):
					best = -1 # initialise it to a small number
					bestsofar = -1 # the index of the best so far that is not in the ten_best list
					for j in range(Hundred):
						if f[j] >= best and j not in ten_best:
							best = f[j]
							bestsofar = j
					ten_best.append(bestsofar)
				# print ('\nthe ten best are', ten_best)

				new_population = []
				for i in ten_best:
					new_population.append(copy.copy(population[i]))

				# d) fill the remaining 90 positions with offspring using fitness proportinate
				prob = []
				sum_f = sum(f)
				for bst in ten_best:
					sum_f -= f[bst]

				for i in range (Hundred): # for the other 90, we will do a bit of magic
				# https://en.wikipedia.org/wiki/Fitness_proportionate_selection
					if i in ten_best:
						prob.append(0)
					else:
						prob.append(f[i]/sum_f)

				# print ('the probability is ', prob)
				
				selected = []
				for i in range (90):
					#select according to probability
					r = 0
					while r == 0:
						r = random.random()
					acc = 0
					j = 0
					while j < Hundred: 
						acc += prob[j] 
						if acc >= r :
							selected.append(j)
							# then this is the selected one
							c = copy.copy(population[j])
							c.evolve()
							new_population.append(c)# asexual reproduction
							j = Hundred
						j+=1
				# print ('\n the other ninty are ', selected)
				population =  new_population
			# 3) If highest-scoring individual ^s in population beats N, then update memory with ^s
			w = []
			best = population[0]
			best_value = -1
			for p in population:
				poff = p.expectedPayoff(self.piN)
				w.append(poff)
				if poff  > 0:
					best = p
					best_value = poff

			if (best_value > 0):
				print ('************************* Here I will replace! *************************')
				self.piN = copy.copy(best)
				self.N = self.piN.support()
				termi = 0
				print ('*******The new one is:   \n', self.piN)
			else:
				termi += 1
			epoch += 1
			mean.append(sum(w)/ len(w))
			index = int(len(w)/2)
			median.append(sorted(w)[index])


		# 4) go to step 1.

		print ('finally, the best strategy we got is: ', self.piN, '  after ', len(mean), ' iterations')
		return (mean, median)
	# def solve(self, WNM):
	# 	# WNM is a list of pure strategies
	# 	# create a matrix
	# 	size = len(WNM)
	# 	M = []
	# 	for i in WNM:
	# 		# print ('row:', i)
	# 		r = [] # a row
	# 		for j in WNM:
	# 			# print ('\tcolumn', j)
	# 			r.append(self.payoff(i, j))
	# 		M.append(r)
	# 	# print (M)

	# 	# TODO : Robert needs to document these
	# 	prob = LpProblem("solve", LpMaximize) # the row player is always trying to maximise

	# 	# define size-many variables
	# 	variables = []
	# 	for w in WNM:
	# 		x = LpVariable('y'+str(w.value), 0, 1)
	# 		variables.append(x)

	# 	v = LpVariable("v", 0)

	# 	# Objective
	# 	prob += v

	# 	# Constraints
	# 	for row in M:
	# 		acc = 0
	# 		for i in range(size):
	# 			acc += row[i] * variables[i]
	# 		prob += v <= acc # the column player will always want to minimise

	# 	acc = 0
	# 	for x in variables:
	# 		acc += x
	# 	prob += acc == 1


	# 	GLPK().solve(prob)
	# 	print ('------------------solving-------------------------')
	# 	# Solution
	# 	values = []
	# 	probabilities = []
	# 	for v in prob.variables():
	# 		for w in WNM:
	# 			if v.name == 'y'+ str(w.value) and v.varValue != 0:
	# 				values.append(w.value)
	# 				probabilities.append(v.varValue)
	# 	print ("objective=", value(prob.objective))

	# 	self.piN = MixedStrategy(values, probabilities)




	# def searchWithHeuristic(self, num):
	# 	strategies = []
	# 	for n in range(num):
	# 		# obtain a mixed strategy of random size
	# 		size = random.randrange(1, len(self.pureStrategies)+1) # any number between 1 and len(self.pureStragegies)
	# 		# print('size',size)
	# 		# st = [] # the pure strategy 
	# 		pc = {} # the percentage
	# 		#initialise the dictionary
	# 		for v in self.pureStrategies:
	# 			pc[v.value] = 0

	# 		total = 0
	# 		for i in range(size):
	# 			c = random.choice(self.pureStrategies).value
	# 			rd = random.randint(0, 5)
	# 			pc[c] = pc[c] + rd 
	# 			total += rd
	# 			# print ('total',total)
	# 			# print ('keys ', pc.keys(), ' values ', pc.values(), 'total', total)

	# 		if total == 0:
	# 			# this mixed strategy is of size one
	# 			strategies.append(random.choice(self.pureStrategies).convertToMixed())
	# 		else:
	# 			for v in self.pureStrategies:
	# 				i = v.value
	# 				pc[i] = pc[i]/total
	# 				# print ('so', i, pc[i])
	# 			strategies.append(MixedStrategy(list(pc.keys()), list(pc.values())))

	# 	return strategies




	# def play(self):
	# 	return self.piN