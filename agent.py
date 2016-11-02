# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

import random

from pulp import *
from strategy import *
import sys



class Agent: # the default one is a Naive agent playing simple a strategy
	name = 'example'
	pureStrategies = []
	N = []
	M = []
	piN = 0
	# payoff  function
	def __init__ (self, name, pureStrategies):
		self.name = name
		self.pureStrategies = pureStrategies
		# at the beginning N is inialised as an arbitrary pure strategy
		self.piN = random.choice(self.pureStrategies).convertToMixed()
		self.N = self.piN.support() 
		# M is initialised as empty list
		self.M = []


	def printInfo(self):
		print ('This agent is called: ', self.name)
		print ('There are the following strategies:')
		for p in self.pureStrategies:
			print ('\t', p)
			
	# every time the searching heuristic returns to the most num strategies.
	# if after termi_num, there is no new winning strategy discovered, we terminate 
	def iteration (self, num, termi_num):
		count = 0 # we consider that we have the solution if for termi_num times the 
		# searching heuristic still does not give us anything new. 
		while count < termi_num:
			print ('\n\n\n\n-----------------the current strategy is\n\t', self.piN)
			print ('----------------discover strategies (T)------------------------')
			T = self.searchWithHeuristic(num)
			# test against piN and obtain the winners
			W = []
			for t in T:
				print ('discovered: ', t)
			print ('-----------------find winning strategies (W)--------------------')
			for t in T:
				if self.payoff (t, self.piN) > 0:
					W.append(t)
					print ('winner: ', t)
			if len(W) != 0:
				print('------------------find N+M+W ------------------------------')
				# solve and find the piN'
				# set union N, M, W
				for n in self.N:
					print ('N', n)
				for m in self.M:
					print ('M', m)
				l = []
				for w in W:
					l += w.support()
				print ('=====')

				WNM = l + self.N + self.M
				# remove duplicates
				WNM2 = []
				for i in range(len(WNM)):
					flag = False
					for w in WNM2:
						if WNM[i].value == w.value:
							flag = True
					if flag == False:
						WNM2.append(WNM[i])
				for a in WNM2:
					print ('W+N+M: ', a)
				WNM = WNM2

				print ('---------------- use linear programming and solve --------')
				self.solve(WNM)
				print ('----------------the updated piN is ------------------')
				print (self.piN)
				self.N = self.piN.support()

				for n in self.N:
					print ('N', n)
				self.M = []
				for m in WNM :
					# if it is in N, remove
					flag = False
					for n in self.N:
						if m.value == n.value:
							flag = True
					if not flag :
						self.M.append(m)
						
				for m in self.M:
					print ('M', m) 


			else:
				print ('There is no winning strategy, skip this turn: ', count)
				count += 1
		print ('The final strategy is: ', self.piN)


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