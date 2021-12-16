from os.path import join
from scipy.io.wavfile import read
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt
import frame
import ste
import pitch

FILE_PATH_THHL = 'D:\Documents\XLTHS\Thi CK\TinHieuHuanLuyen'
FILE_WAV_THHL = ['01MDA.wav', '02FVA.wav', '03MAB.wav', '06FTB.wav']
FILE_LAB_THHL = ['01MDA.lab', '02FVA.lab', '03MAB.lab', '06FTB.lab']

FILE_PATH_THKT = 'D:\Documents\XLTHS\Thi CK\TinHieuKiemThu'
FILE_WAV_THKT = ['30FTN.wav', '42FQT.wav', '44MTT.wav', '45MDV.wav']
FILE_LAB_THKT = ['30FTN.lab', '42FQT.lab', '44MTT.lab', '45MDV.lab']

LINE = [[0.59, 0.97, 1.76, 2.11, 3.44, 3.77, 4.70, 5.13, 5.96, 6.28], 
        [0.46, 0.99, 1.56, 2.13, 2.51, 2.93, 3.79, 4.38, 4.77, 5.22], 
        [0.93, 1.42, 2.59, 3.0, 4.71, 5.11, 6.26, 6.66, 8.04, 8.39], 
        [0.88, 1.34, 2.35, 2.82, 3.76, 4.13, 5.04, 5.50, 6.41, 6.79]]

SPEECH_INDEX = [73, 73, 120, 110]
SILENCE_INDEX = [110, 110, 90, 160]

INDEX = 0
TIME_FRAME = 0.03

# Main
for i in range(0, len(FILE_WAV_THKT)):
  frequency, signal = read(join(FILE_PATH_THKT, FILE_WAV_THKT[i]))
  
  signal = signal / max(np.max(signal), abs(np.min(signal)))
  frameLength = int(TIME_FRAME * frequency) # Độ dài của 1 frame (đơn vị mẫu)
  framesArray = frame.getFramesArray(signal, frameLength)
  STEArray = ste.calSTE(framesArray)
  markPoint = ste.findSpeechAndSilence(STEArray)
  
  timeSample = np.zeros(len(signal))
  for index in range(len(signal)):
    timeSample[index] = index / frequency
    
  timeSampleSTE = np.zeros(len(STEArray))
  for index in range(len(STEArray)):
    timeSampleSTE[index] = TIME_FRAME * index / 3
  
  F0 = np.zeros(len(framesArray))
  timeSampleF0 = np.zeros(len(framesArray))
  for index in range(len(framesArray)):
      F0[index] = pitch.getPitch(index, frequency, framesArray, frameLength, markPoint)
      timeSampleF0[index] = TIME_FRAME * index / 3  
      
  F0mean = np.mean([value for value in F0 if value > 0 and value < 450])
  F0std = np.std([value for value in F0 if value > 0 and value < 450])
  
  hamming = np.hamming(frameLength)
  fs = np.linspace(0, frequency / 2, 2 ** 12)
  speechFrame = framesArray[SPEECH_INDEX[i]] * hamming
  speechSpectrum = abs(np.fft.fft(speechFrame, 2 ** 13))[:2 ** 12]
  peaks, _  = find_peaks(speechSpectrum, distance=10, prominence=8.5)
  fsPeaks = [peak * frequency / (2 * len(speechSpectrum)) for peak in peaks]
  silenceFrame = framesArray[SILENCE_INDEX[i]] * hamming
  silenceSpectrum = abs(np.fft.fft(silenceFrame, 2 ** 13))[:2 ** 12]
  
  # Show
  plt.figure(i + 1)
  plt.subplot(4, 1, 1)
  plt.title(f"Signal: {FILE_WAV_THKT[i]}")
  plt.plot(timeSample, signal)
  plt.plot(timeSampleSTE, STEArray, 'r')
  plt.axhline(y=0.04772, color='orange', linestyle='-')
  for line in LINE[i]:
    plt.axvline(line, color = 'g')
  for index in range(1, len(markPoint)):
    if markPoint[index] == 1 and markPoint[index - 1] == 0 or markPoint[index] == 0 and markPoint[index - 1] == 1:
      plt.axvline(x = TIME_FRAME * index / 3, color = 'b', linestyle = 'dashed')
  plt.legend(['Signal', 'STE', 'Threshold'])
  plt.xlabel('Time(s)')
  plt.ylabel('Signal Amplitude')
  plt.subplot(4, 1, 2)
  plt.title(f"F0 FFT - F0mean = {round(F0mean, 2)}, F0std = {round(F0std, 2)}")
  plt.ylim([0, 450])
  plt.plot(timeSampleF0, F0, '.')
  plt.xlabel('Time(s)')
  plt.ylabel('Frequence(Hz)')
  plt.subplot(4, 1, 3)
  plt.title('Middle result: Speech Spectrum')
  plt.plot(fsPeaks, speechSpectrum[peaks], "vg")
  plt.plot(fs, speechSpectrum)
  plt.xlabel('Frequence(Hz)')
  plt.ylabel('Amplitude')
  plt.subplot(4, 1, 4)
  plt.title('Middle result: Silence Spectrum')
  plt.plot(fs, silenceSpectrum)
  plt.xlabel('Frequence(Hz)')
  plt.ylabel('Amplitude')
  plt.tight_layout()
plt.show()