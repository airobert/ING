# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

from agent import *
import random
import sys
from strategy import *

		
def main():

	playING (1, 2, 0) # k, n, sigma
	a = Agent(k, n, sigma)
	a.play()

if __name__ == "__main__":
	main()