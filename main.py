# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

from agent import *
import random
import sys
from strategy import *


rounds = 5 # how many rounds of games do we iterate
# repeat = 10 # repeat ten times for each round and calculate the average payoff

ROCK = 0
PAPER = 1
SCISSORS = 2

class  Platform(object):
	
	def __init__(self, agents, domain):
		self.agents = agents
		self.domain = domain # for now, this is always 3, so hardcoded
		for a in agents:
			a.payoff = self.expectedPayoff

	# the expected payoff for (pure strategy c1 against c2)
	def payoff (self, c1, c2): # zero sum game
		# rock = 0, paper = 1, scissors = 2
		# +-------------------------------------------+
		# |           | rock 0 | paper 1 | scissors 2 |  
		# | rock 0    |      0 |      -1 |          1 |
		# | paper 1   |      1 |       0 |         -1 |
		# | scissors 2|     -1 |       1 |          0 |
		# +-------------------------------------------+  

		matrix = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]

		return matrix[c1][c2]


	def expectedPayoff (self, m ,n):
		# m and n can be pure or mixed strategies but here we use a uniform implementation
		# if m or n is pure strategy, then convert it to a mixed strategy and evaluate

		if 'PureStrategy' in str(type(m)):
			m = m.convertToMixed()

		if 'PureStrategy' in  str(type(n)):
			n = n.convertToMixed()

		em = 0 # expected payoff for m
		for i in range(len(m.values)):
			e = 0
			for j in range(len(n.values)):
				e += self.payoff(m.values[i], n.values[j])* n.probabilities[j]
			em += e * m.probabilities[i]
		return em


		
def main():

	r = PureStrategy(ROCK)
	s = PureStrategy(ROCK)
	print (r == s)
	m = MixedStrategy([1,2], [0.3, 0.7])
	n = MixedStrategy([1,2], [0.5, 0.5])
	s = MixedStrategy([1,2], [0.5, 0.5])
	print (m == n)
	print (s == n)

	l = [m, n]
	l.remove (s)
	for i in l:
		print (i)
	
if __name__ == "__main__":
	main()