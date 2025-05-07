import numpy as np
import os
from scipy.io import wavfile
import zipfile

from synthesize_with_overtones.wave_file_generator import SumOfSinesWaveDefinition
from synthesize_with_overtones.wave_file_generator import ListOfSumOfOvertonesStrategies
from synthesize_with_overtones.wave_file_generator import RandomPhaseStrategy
from synthesize_with_overtones.wave_file_generator import StandardPhaseStrategy
from synthesize_with_sample_sequences.wave_file_generator import SequenceOfSamplesWaveDefinition
from synthesize_with_sample_sequences.wave_file_generator import ListOfSampleStrategies

samplerate = 44100
nameOfOutDir = "./out/"
nameOfZipFile = 'allWavFiles.zip'
filenametemplateFactorStrategy = "sound-{}-{}-{}s-{}hz.wav"
filenametemplateSampleStrategy = "sound-S-{}-{}s-{}hz.wav"

class Params:
	def __init__(self,sineFrequency,durationInSeconds,amplitude):
		self.sineFrequency=sineFrequency
		self.durationInSeconds=durationInSeconds
		self.amplitude=amplitude

class Main:
	def __init__(self):
		self.soundParamsList=[
			Params(sineFrequency=220.0,durationInSeconds=0.8,amplitude=0.3),
		]
		
	def runFactorStrategy(self,params,factorStrategy,phaseStrategies,allTs,soundsZip):
		for phaseStrategy in phaseStrategies:
			waveDefinition = SumOfSinesWaveDefinition(params,factorStrategy,phaseStrategy)
			data = waveDefinition.toneAtAllTs(allTs)
			filename = filenametemplateFactorStrategy.format(
				phaseStrategy.getName(),factorStrategy.getName(),params.durationInSeconds,params.sineFrequency)
			wavfile.write(filename, samplerate, data.astype(np.float32))
			soundsZip.write(filename)
			
	def runSampleStrategy(self,params,sampleStrategy,allTs,soundsZip):
		waveDefinition = SequenceOfSamplesWaveDefinition(params,sampleStrategy)
		data = waveDefinition.toneAtAllTs(allTs)
		filename = filenametemplateSampleStrategy.format(sampleStrategy.getName(),params.durationInSeconds,params.sineFrequency)
		wavfile.write(filename, samplerate, data.astype(np.float32))
		soundsZip.write(filename)
	
	def run(self):
		os.makedirs(nameOfOutDir, exist_ok=True)
		os.chdir(nameOfOutDir)
		factorStrategies = ListOfSumOfOvertonesStrategies.getAllStrategies()
		sampleStrategies = ListOfSampleStrategies.getAllStrategies()
		phaseStrategies=[StandardPhaseStrategy(),RandomPhaseStrategy()]
		with zipfile.ZipFile(nameOfZipFile, 'w') as soundsZip:
			for params in self.soundParamsList:
				allTs = np.linspace(0.0, params.durationInSeconds, num=int(samplerate*params.durationInSeconds))
				for factorStrategy in factorStrategies:
					self.runFactorStrategy(params,factorStrategy,phaseStrategies,allTs,soundsZip)
				for sampleStrategy in sampleStrategies:
					self.runSampleStrategy(params,sampleStrategy,allTs,soundsZip)
			soundsZip.close()
			
Main().run()
