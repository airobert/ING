# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

class PureStrategy(object):
	def __init__(self, value):
		self.value = value

	def convertToMixed(self):
		return MixedStrategy([self.value], [1.0])

	def __str__(self): # override the default printing function
		return self.value

	def __eq__(self, other): 
		return (self.value == other.value)

# WARNING!!!!
# I have just changed the strategy to a dictionary

class MixedStrategy(object):
	d = {}
	def __init__(self, values, probabilities):
		if len(values) == len(probabilities) and 1 - sum(probabilities) < 0.0001 :
			for i in range (len(values)):
				self.d[values[i]] = probabilities[i]
		else:
			print ('error', values, probabilities, sum(probabilities)) # TODO: make this an exception
		
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

	