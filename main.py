import numpy as np
import os
from scipy.io import wavfile
import zipfile

from synthesize_with_overtones.wave_file_generator import Params
from synthesize_with_overtones.wave_file_generator import SumOfSinesWaveDefinition
from synthesize_with_overtones.wave_file_generator import SumOfSamplesWaveDefinition
from synthesize_with_overtones.wave_file_generator import ListsOfStrategies
from synthesize_with_overtones.wave_file_generator import RandomPhaseStrategy
from synthesize_with_overtones.wave_file_generator import StandardPhaseStrategy

samplerate = 44100
nameOfOutDir = "./out/"

paramsList=[
	Params(sineFrequency=110.0,durationInSeconds=0.3,amplitude=0.3),
]

os.makedirs(nameOfOutDir, exist_ok=True)
os.chdir(nameOfOutDir)
factorStrategies = ListsOfStrategies.getAllFactorStrategies()
sampleStrategies = ListsOfStrategies.getAllSampleStrategies()
with zipfile.ZipFile('allWavFiles.zip', 'w') as soundsZip:
	for params in paramsList:
		durationInSeconds = params.durationInSeconds
		filenametemplateFactorStrategy = "sound-F-{}-{}-{}s-{}hz.wav"
		filenametemplateRandomPhase = "sound-FR-{}-{}-{}s-{}hz.wav"
		filenametemplateSampleStrategy = "sound-S-{}-{}-{}s-{}hz.wav"
		allTs = np.linspace(0.0, durationInSeconds, num=int(samplerate*durationInSeconds))
		filenames = []
		i = 0
		for strategy in factorStrategies:
			waveDefinition1 = SumOfSinesWaveDefinition(params,strategy,StandardPhaseStrategy())
			waveDefinition2 = SumOfSinesWaveDefinition(params,strategy,RandomPhaseStrategy())
			data = waveDefinition1.toneAtAllTs(allTs)
			dataWithRandomOvertonePhases = waveDefinition2.toneAtAllTs(allTs)
			i = i+1
			# to do: more DRY principle here:
			filename1 = filenametemplateFactorStrategy.format(i,strategy.getName(),durationInSeconds,params.sineFrequency)
			filename2 = filenametemplateRandomPhase.format(i,strategy.getName(),durationInSeconds,params.sineFrequency)
			wavfile.write(filename1, samplerate, data.astype(np.float32))
			wavfile.write(filename2, samplerate, dataWithRandomOvertonePhases.astype(np.float32))
			soundsZip.write(filename1)
			soundsZip.write(filename2)
		for strategy in sampleStrategies:
			waveDefinition = SumOfSamplesWaveDefinition(params,strategy)
			data = waveDefinition.toneAtAllTs(allTs)
			filename = filenametemplateSampleStrategy.format(i,strategy.getName(),durationInSeconds,params.sineFrequency)
			wavfile.write(filename, samplerate, data.astype(np.float32))
			soundsZip.write(filename)
	soundsZip.close()
