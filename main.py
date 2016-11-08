# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

from agent import *
import random
import sys
from strategy import *

import numpy as np
import matplotlib.pyplot as plt

import datetime

		
def main():
	meanM = []
	TERMI = 40
	ITER = 10

	# for i in range (ITER):
	# 	a = Agent(100,2,0)
	# 	mean = a.playBOG(TERMI)
	# 	print (mean)
	# 	# t = range(len(mean))
	# 	# for i in range (10):
	# 	# m = MixedStrategy(10,2,3)
	# 	# print (m, ' = ', m.mean(), ' ', m.median())
	# 	meanM.append(mean)
	# smallest = 10000
	# for m in meanM:
	# 	if len(m) < smallest:
	# 		smallest = len(m)

	# M =[]
	# for t in range (smallest):
	# 	mS = 0
	# 	for m in meanM:
	# 		mS += m[t]
	# 	M.append(mS/ITER)

	# t =  range(smallest)
	# print(datetime.datetime.now())
	# plt.plot(t, M, 'r--')
	# plt.show()	


 	# the following is corresponding to the nash memory version of this game

	a = Agent (100, 2, 0)
	(mean, median) = a.playNash(TERMI)



if __name__ == "__main__":
	main()