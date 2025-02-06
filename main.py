import numpy as np
import os
from scipy.io import wavfile
import zipfile

from synthesize_with_overtones.wave_file_generator import Params
from synthesize_with_overtones.wave_file_generator import WaveDefinition
from synthesize_with_overtones.wave_file_generator import ListsOfStrategies

samplerate = 44100
nameOfOutDir = "./out/"

paramsList=[
	Params(sineFrequency=110.0,durationInSeconds=0.5,amplitude=0.3),
]

os.makedirs(nameOfOutDir, exist_ok=True)
os.chdir(nameOfOutDir)
strategies = ListsOfStrategies.getAllStrategies()
with zipfile.ZipFile('allWavFiles.zip', 'w') as soundsZip:
	for params in paramsList:
		durationInSeconds = params.durationInSeconds
		filenametemplate = "sound{}-{}-{}s-{}hz.wav"
		allTs = np.linspace(0.0, durationInSeconds, num=int(samplerate*durationInSeconds))
		filenames = []
		i = 0
		for strategy in strategies:
			waveDefinition = WaveDefinition(params,strategy)
			data = waveDefinition.toneAtAllTs(allTs)
			i = i+1
			filename = filenametemplate.format(i,strategy.getName(),durationInSeconds,params.sineFrequency)
			wavfile.write(filename, samplerate, data.astype(np.float32))
			soundsZip.write(filename)
	soundsZip.close()
