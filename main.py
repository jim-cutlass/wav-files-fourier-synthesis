import numpy as np
import os
from scipy.io import wavfile
import zipfile

from synthesize_with_overtones.wave_file_generator import Params
from synthesize_with_overtones.wave_file_generator import SumOfSinesWaveDefinition
from synthesize_with_overtones.wave_file_generator import SequenceOfSamplesWaveDefinition
from synthesize_with_overtones.wave_file_generator import ListsOfStrategies
from synthesize_with_overtones.wave_file_generator import RandomPhaseStrategy
from synthesize_with_overtones.wave_file_generator import StandardPhaseStrategy

samplerate = 44100
nameOfOutDir = "./out/"

paramsList=[
	Params(sineFrequency=110.0,durationInSeconds=0.2,amplitude=0.3),
]

os.makedirs(nameOfOutDir, exist_ok=True)
os.chdir(nameOfOutDir)
factorStrategies = ListsOfStrategies.getAllFactorStrategies()
sampleStrategies = ListsOfStrategies.getAllSampleStrategies()
with zipfile.ZipFile('allWavFiles.zip', 'w') as soundsZip:
	# TO DO: refactor: less for-loops here:
	for params in paramsList:
		durationInSeconds = params.durationInSeconds
		filenametemplateFactorStrategy = "sound-{}-{}-{}-{}s-{}hz.wav"
		filenametemplateSampleStrategy = "sound-S-{}-{}-{}s-{}hz.wav"
		allTs = np.linspace(0.0, durationInSeconds, num=int(samplerate*durationInSeconds))
		filenames = []
		i = 0
		phaseStrategies=[StandardPhaseStrategy(),RandomPhaseStrategy()]
		for factorStrategy in factorStrategies:
			i = i+1
			for phaseStrategy in phaseStrategies:
				waveDefinition = SumOfSinesWaveDefinition(params,factorStrategy,phaseStrategy)
				data = waveDefinition.toneAtAllTs(allTs)
				filename = filenametemplateFactorStrategy.format(
					i,phaseStrategy.getName(),factorStrategy.getName(),durationInSeconds,params.sineFrequency)
				wavfile.write(filename, samplerate, data.astype(np.float32))
				soundsZip.write(filename)
		for strategy in sampleStrategies:
			waveDefinition = SequenceOfSamplesWaveDefinition(params,strategy)
			data = waveDefinition.toneAtAllTs(allTs)
			filename = filenametemplateSampleStrategy.format(i,strategy.getName(),durationInSeconds,params.sineFrequency)
			wavfile.write(filename, samplerate, data.astype(np.float32))
			soundsZip.write(filename)
	soundsZip.close()
