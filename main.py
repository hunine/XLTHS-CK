from os.path import join
from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt

FILE_PATH_THHL = 'D:\Documents\XLTHS\Thi CK\TinHieuHuanLuyen'
FILE_WAV_THHL = ['01MDA.wav', '02FVA.wav', '03MAB.wav', '06FTB.wav']
FILE_LAB_THHL = ['01MDA.lab', '02FVA.lab', '03MAB.lab', '06FTB.lab']

FILE_PATH_THKT = 'D:\Documents\XLTHS\Thi CK\TinHieuKiemThu'
FILE_WAV_THKT = ['30FTN.wav', '42FQT.wav', '44MTT.wav', '45MDV.wav']
FILE_LAB_THKT = ['30FTN.lab', '42FQT.lab', '44MTT.lab', '45MDV.lab']
INDEX = 0
TIME_FRAME = 0.03

# Chia Frame
def getFramesArray(signal, frameLength):
  step = frameLength // 3
  frames = []
  index = 0
  for i in range(0, len(signal) // step):
    temp = signal[index : index + frameLength]
    frames.append(temp)
    index += step
  return frames

# Hàm tính STE
def STE(framesArray):
  ste = np.zeros(len(framesArray))
  
  for i in range(len(framesArray)):
    ste[i] = np.sum(framesArray[i]**2)
  ste = ste / np.max(ste)
  
  return ste

# Phân biệt đoạn tiếng nói và đoạn khoảng lặng
def findSpeechAndSilence(STEArray, threshold = 0.03):
  markSpeech = np.zeros(len(STEArray))
  
  for i in range(len(STEArray)):
    if STEArray[i] >= threshold:
      markSpeech[i] = 1
  
  # Kiểm tra khoảng lặng > 300ms
  countZero = 1
  firstPosition = 0
  for i in range(1, len(markSpeech)):
    if markSpeech[i] == 0 and markSpeech[i - 1] == 0:
      countZero += 1
    elif markSpeech[i] == 1 and markSpeech[i - 1] == 0:
      if countZero < 10:
        for j in range(firstPosition, i):
          markSpeech[j] = 1
      countZero = 1
    elif markSpeech[i] == 0 and markSpeech[i - 1] == 1:
      firstPosition = i
  
  return markSpeech

# Main
for i in range(0, len(FILE_WAV_THHL)):
  frequency, signal = read(join(FILE_PATH_THHL, FILE_WAV_THHL[i]))
  
  signal = signal / max(np.max(signal), abs(np.min(signal)))
  frameLength = int(TIME_FRAME * frequency) # Độ dài của 1 frame (đơn vị mẫu)
  framesArray = getFramesArray(signal, frameLength)
  STEArray = STE(framesArray)
  markPoint = findSpeechAndSilence(STEArray)
  
  timeSample = np.zeros(len(signal))
  for index in range(len(signal)):
    timeSample[index] = index / frequency
    
  timeSampleSTE = np.zeros(len(STEArray))
  for index in range(len(STEArray)):
    timeSampleSTE[index] = TIME_FRAME * index / 3
    
  # Show
  plt.figure(i + 1)
  plt.title(f"Signal: {FILE_WAV_THHL[i]}")
  plt.plot(timeSample, signal)
  plt.plot(timeSampleSTE, STEArray, 'r')
  for i in range(1, len(markPoint)):
    if markPoint[i] == 1 and markPoint[i - 1] == 0 or markPoint[i] == 0 and markPoint[i - 1] == 1:
      plt.axvline(x = TIME_FRAME * i / 3, color = 'b')
  
plt.show()
