# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

from agent import *
import random
import sys
from strategy import *

import numpy as np
import matplotlib.pyplot as plt

		
def main():

	a = Agent(10,2,5)
	mean = a.iteration(3)
	print (mean)
	t = range(len(mean))
	# for i in range (10):
	# m = MixedStrategy(10,2,3)
	# print (m, ' = ', m.mean(), ' ', m.median())
	plt.plot(t, mean, 'r--')
	plt.show()	

if __name__ == "__main__":
	main()