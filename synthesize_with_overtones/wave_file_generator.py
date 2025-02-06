from abc import ABC, abstractmethod
import math
import numpy as np

maxHarmonicNumber = 1000
moveFactorForThirds = ((2.0**(1/12.0))**4.0)/(5/4)
moveFactorForFifths = ((2.0**(1/12.0))**7.0)/(3/2)
moveFactorForNaturalSevenths = ((2.0**(1/12.0))**10.0)/(7/4)

class Params:
	def __init__(self,sineFrequency,durationInSeconds,amplitude):
		self.sineFrequency=sineFrequency
		self.durationInSeconds=durationInSeconds
		self.amplitude=amplitude

class FactorStrategy(ABC):
	@abstractmethod
	def getFactor(self,harmonicNumber):
		pass
	@abstractmethod
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		pass
	def getName(self):
		return type(self).__name__
	
class Factor0Strategy(FactorStrategy):
	def getFactor(self,harmonicNumber):
		return 0.0
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		return originalOvertonePosition
	
class Factor1Strategy(FactorStrategy):
	def getFactor(self,harmonicNumber):
		return 1.0
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		return originalOvertonePosition
	
class AlternatingStatefulStrategy(FactorStrategy):
	def __init__(self):
		self.factor=1.0
	# getFactor must be called in order (first for harmonic number 1, then second harmonic number 2 and so on)
	def getFactor(self,harmonicNumber):
		returnValue = self.factor
		self.factor = -self.factor
		return returnValue
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		return originalOvertonePosition

class AlternatingSquareWaveStatefulStrategy(FactorStrategy):
	def __init__(self):
		self.factorParam = 0
	def mapParam4ToFactor(self,factor4param):
		match factor4param:
			case 0 | 2:
				return 0.0
			case 1:
				return -1.0
			case 3:
				return 1.0
		return 0.0
	def getFactor(self,harmonicNumber):
		returnValue = self.mapParam4ToFactor(self.factorParam)
		self.factorParam = (self.factorParam + 1) if (self.factorParam < 3) else 0
		return returnValue
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		return originalOvertonePosition
		
class UseOnly2or3or5multiplesStrategy(FactorStrategy):
	def getFactor(self,harmonicNumber):
		if harmonicNumber % 7 == 0:
			return 0.0
		if harmonicNumber % 11 == 0:
			return 0.0
		if harmonicNumber % 13 == 0:
			return 0.0
		if harmonicNumber % 17 == 0:
			return 0.0
		if harmonicNumber % 19 == 0:
			return 0.0
		if harmonicNumber % 23 == 0:
			return 0.0
		if harmonicNumber % 29 == 0:
			return 0.0
		# to do: take care of the other primes here
		return 1.0
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		return originalOvertonePosition
		
class FilterOutTheNaturalSeventhsStrategy(FactorStrategy):
	def getFactor(self,harmonicNumber):
		if harmonicNumber % 7 == 0:
			return 0.0
		return 1.0
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		return originalOvertonePosition
		
class FilterOutTheFifthsStrategy(FactorStrategy):
	def getFactor(self,harmonicNumber):
		if harmonicNumber % 3 == 0:
			return 0.0
		return 1.0
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		return originalOvertonePosition
		
class AddHalfNumberedOvertonesStrategy(FactorStrategy):
	def getFactor(self,harmonicNumber):
		return 1.0
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		return 0.5 * originalOvertonePosition
	
class UseEveryNthHarmonicStatefulStrategy(FactorStrategy):
	def __init__(self,n):
		self.theNInNth = n
		self.factorParam = 0
	def getFactor(self,harmonicNumber):
		returnValue = 1.0 if (self.factorParam == (self.theNInNth-1)) else 0.0
		self.factorParam = (self.factorParam + 1) if (self.factorParam < (self.theNInNth-1)) else 0
		return returnValue
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		return originalOvertonePosition
	def getName(self):
		return type(self).__name__+"-"+str(self.theNInNth)

class StretchedFactor1Strategy(FactorStrategy):
	def __init__(self,overtoneStretchFactor):
		self.overtoneStretchFactor = overtoneStretchFactor
	def getFactor(self,harmonicNumber):
		return 1.0
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		return originalOvertonePosition*self.overtoneStretchFactor
	def getName(self):
		return type(self).__name__+str(self.overtoneStretchFactor)

class StretchedAndMovedFactor1Strategy(FactorStrategy):
	def __init__(self,overtoneStretchFactor,overtoneMoveAddition):
		self.overtoneStretchFactor = overtoneStretchFactor
		self.overtoneMoveAddition = overtoneMoveAddition
	def getFactor(self,harmonicNumber):
		return 1.0
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		return originalOvertonePosition*self.overtoneStretchFactor + self.overtoneMoveAddition
	def getName(self):
		return type(self).__name__+"_"+str(self.overtoneStretchFactor)+"_"+str(self.overtoneMoveAddition)
		
class StretchThirdsToTemperedFactorStrategy(FactorStrategy):
	def getFactor(self,harmonicNumber):
		return 1.0
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		if not type(originalOvertonePosition) is int:
			raise TypeError("Only integers are allowed as arguments for the method getShiftedOvertonePosition")
		if math.fmod(originalOvertonePosition,5) == 0:
  			return originalOvertonePosition * moveFactorForThirds
		else:
			return originalOvertonePosition
			
class ShrinkFifthsToTemperedFactorStrategy(FactorStrategy):
	def getFactor(self,harmonicNumber):
		return 1.0
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		if not type(originalOvertonePosition) is int:
			raise TypeError("Only integers are allowed as arguments for the method getShiftedOvertonePosition")
		if math.fmod(originalOvertonePosition,3) == 0:
  			return originalOvertonePosition * moveFactorForFifths
		else:
			return originalOvertonePosition
			
class StretchNaturalSeventhsToTemperedFactorStrategy(FactorStrategy):
	def getFactor(self,harmonicNumber):
		return 1.0
	def getShiftedOvertonePosition(self,originalOvertonePosition):
		if not type(originalOvertonePosition) is int:
			raise TypeError("Only integers are allowed as arguments for the method getShiftedOvertonePosition")
		if math.fmod(originalOvertonePosition,7) == 0:
  			return originalOvertonePosition * moveFactorForNaturalSevenths
		else:
			return originalOvertonePosition
			
class ListsOfStrategies:
	def getAllStrategies():
		return [
			Factor1Strategy(),
			AlternatingStatefulStrategy(),
			UseEveryNthHarmonicStatefulStrategy(2),
			AlternatingSquareWaveStatefulStrategy(),
			UseOnly2or3or5multiplesStrategy(),
			UseEveryNthHarmonicStatefulStrategy(3),
			Factor0Strategy(),
			StretchedFactor1Strategy(2.0),
			StretchedAndMovedFactor1Strategy(2.0,-1),
			StretchThirdsToTemperedFactorStrategy(),
			ShrinkFifthsToTemperedFactorStrategy(),
			StretchNaturalSeventhsToTemperedFactorStrategy(),
			FilterOutTheNaturalSeventhsStrategy(),
			FilterOutTheFifthsStrategy(),
			AddHalfNumberedOvertonesStrategy(),
		]

class WaveDefinition:
	def __init__(self, params, strategy):
		self.params = params
		self.strategy = strategy
	def toneAtAllTs(self,allTs):
		allPhasesOfBaseFrequency = 2.0 * np.pi * self.params.sineFrequency * allTs
		sumsOfHarmonics = np.sin(allPhasesOfBaseFrequency)
		for overtonePosition in range(2,maxHarmonicNumber):
			possiblyChangedOvertonePosition = self.strategy.getShiftedOvertonePosition(overtonePosition)
			addedValue = \
				(1.0/possiblyChangedOvertonePosition)*np.sin(possiblyChangedOvertonePosition*2.0*np.pi*self.params.sineFrequency*allTs)
			sumsOfHarmonics += self.strategy.getFactor(overtonePosition) * addedValue
		return self.params.amplitude * sumsOfHarmonics
