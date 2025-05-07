from abc import ABC, abstractmethod
import math
import numpy as np
import random
		
class SampleStrategy(ABC):
	@abstractmethod
	def getSampleValue(self,phase):
		pass
	def getName(self):
		return type(self).__name__
		
class SineSampleStrategy(SampleStrategy):
	def getSampleValue(self, phase):
		return math.sin(phase)

class OctaveDoubleSineSampleStrategy(SampleStrategy):
	def getSampleValue(self, phase):
		structuringSine = math.sin(phase*0.25)
		if structuringSine >= 0.0:
			return 0.5*math.sin(phase)
		else:
			return (-1.0)*math.sin((phase - 2.0*math.pi)*0.5)
			
class ListOfSampleStrategies:
	def getAllStrategies():
		return [
			SineSampleStrategy(),
			OctaveDoubleSineSampleStrategy()
		]

class SequenceOfSamplesWaveDefinition:
	def __init__(self, params, strategy):
		self.params = params
		self.strategy = strategy
	def toneAtAllTs(self,allTs):
		result = []
		allPhasesOfBaseFrequency = 2.0 * np.pi * self.params.sineFrequency * allTs
		for phase in allPhasesOfBaseFrequency.tolist():
			result.append(self.toneAtPhase(phase))
		return np.array(result)
	def toneAtPhase(self,phase):
		sequenceOfSamples=self.strategy.getSampleValue(phase)
		return self.params.amplitude * sequenceOfSamples
