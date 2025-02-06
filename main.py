import numpy as np
import os
from scipy.io import wavfile
import zipfile

from synthesize_with_overtones.wave_file_generator import Params
from synthesize_with_overtones.wave_file_generator import WaveDefinition
from synthesize_with_overtones.wave_file_generator import Factor1Strategy, AlternatingStatefulStrategy, UseEveryNthHarmonicStatefulStrategy, AlternatingSquareWaveStatefulStrategy, UseOnly2or3or5multiplesStrategy, UseEveryNthHarmonicStatefulStrategy, Factor0Strategy, StretchedFactor1Strategy,StretchedAndMovedFactor1Strategy, StretchThirdsToTemperedFactorStrategy, ShrinkFifthsToTemperedFactorStrategy, StretchNaturalSeventhsToTemperedFactorStrategy, FilterOutTheNaturalSeventhsStrategy, FilterOutTheFifthsStrategy, AddHalfNumberedOvertonesStrategy

samplerate = 44100
nameOfOutDir = "./out/"

paramsList=[
	Params(sineFrequency=110.0,durationInSeconds=0.3,amplitude=0.30),
]

os.makedirs(nameOfOutDir, exist_ok=True)
os.chdir(nameOfOutDir)
strategies = [
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
with zipfile.ZipFile('allWavFiles.zip', 'w') as soundsZip:
	for params in paramsList:
		durationInSeconds = params.durationInSeconds
		filenametemplate = "sound-{}-{}s-{}hz.wav"
		allTs = np.linspace(0.0, durationInSeconds, num=int(samplerate*durationInSeconds))
		filenames = []
		i = 0
		for strategy in strategies:
			waveDefinition = WaveDefinition() # to do: put strategy, maybe more, in this line
			data = waveDefinition.toneAtAllTs(params,allTs,strategy)
			i = i+1
			filename = filenametemplate.format(strategy.getName(),durationInSeconds,params.sineFrequency)
			wavfile.write(filename, samplerate, data.astype(np.float32))
			soundsZip.write(filename)
	soundsZip.close()
