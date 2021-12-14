from os.path import join
from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt
import frame
import ste

FILE_PATH_THHL = 'D:\Documents\XLTHS\Thi CK\TinHieuHuanLuyen'
FILE_WAV_THHL = ['01MDA.wav', '02FVA.wav', '03MAB.wav', '06FTB.wav']
FILE_LAB_THHL = ['01MDA.lab', '02FVA.lab', '03MAB.lab', '06FTB.lab']

FILE_PATH_THKT = 'D:\Documents\XLTHS\Thi CK\TinHieuKiemThu'
FILE_WAV_THKT = ['30FTN.wav', '42FQT.wav', '44MTT.wav', '45MDV.wav']
FILE_LAB_THKT = ['30FTN.lab', '42FQT.lab', '44MTT.lab', '45MDV.lab']
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
  
  # Show
  plt.figure(i + 1)
  plt.title(f"Signal: {FILE_WAV_THKT[i]}")
  plt.plot(timeSample, signal)
  plt.plot(timeSampleSTE, STEArray, 'r')
  for i in range(1, len(markPoint)):
    if markPoint[i] == 1 and markPoint[i - 1] == 0 or markPoint[i] == 0 and markPoint[i - 1] == 1:
      plt.axvline(x = TIME_FRAME * i / 3, color = 'b')
  
plt.show()
