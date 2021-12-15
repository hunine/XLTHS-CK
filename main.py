from os.path import join
from scipy.io.wavfile import read
from scipy.signal import find_peaks
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

def getPitch(index, frameLength):
  hamming = np.hamming(frameLength)
  if (markPoint[index] == 1):
    frame = framesArray[index] * hamming
    spt = abs(np.fft.fft(frame, 2 ** 12))[:2 ** 11]
    peaks, _  = find_peaks(spt, distance=10, prominence=8)
    fs = np.linspace(0, frequency / 2, len(spt))
    if len(peaks) >= 3:
      l1 = abs(fs[peaks[0]] - fs[peaks[1]])
      l2 = abs(fs[peaks[1]] - fs[peaks[2]])
      if l1 > 70 and l1 < 400 and l2 > 70 and l2 < 400:
        if l1 > 1.5 * l2:
          return l2
        elif l2 > 1.5 * l1:
          return l1
        return (l1 + l2) / 2
    elif len(peaks) == 2:
      l = abs(fs[peaks[0]] - fs[peaks[1]])
      if l > 70 and l < 400:
        return l
  return 0   

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
      F0[index] = getPitch(index, frameLength)
      timeSampleF0[index] = TIME_FRAME * index / 3  
  
  # Show
  plt.figure(i + 1)
  plt.subplot(4, 1, 1)
  plt.title(f"Signal: {FILE_WAV_THKT[i]}")
  plt.plot(timeSample, signal)
  plt.plot(timeSampleSTE, STEArray, 'r')
  for i in range(1, len(markPoint)):
    if markPoint[i] == 1 and markPoint[i - 1] == 0 or markPoint[i] == 0 and markPoint[i - 1] == 1:
      plt.axvline(x = TIME_FRAME * i / 3, color = 'b')
  plt.subplot(4, 1, 2)
  plt.plot(timeSampleF0, F0, '.')
  plt.subplot(4, 1, 3)
  plt.plot(np.linspace(0, frequency / 2, 2 ** 11))
plt.show()



# x = np.sin(2*np.pi*(2**np.linspace(2,10,1000))*np.arange(1000)/48000) + np.random.normal(0, 1, 1000) * 0.15
# peaks, _ = find_peaks(x, distance=20)
# peaks2, _ = find_peaks(x, prominence=1)      # BEST!
# peaks3, _ = find_peaks(x, width=20)
# peaks4, _ = find_peaks(x, threshold=0.4)     # Required vertical distance to its direct neighbouring samples, pretty useless

# plt.subplot(2, 2, 1)
# plt.plot(peaks, x[peaks], "xr"); plt.plot(x); plt.legend(['distance'])
# plt.subplot(2, 2, 2)
# plt.plot(peaks2, x[peaks2], "ob"); plt.plot(x); plt.legend(['prominence'])
# plt.subplot(2, 2, 3)
# plt.plot(peaks3, x[peaks3], "vg"); plt.plot(x); plt.legend(['width'])
# plt.subplot(2, 2, 4)
# plt.plot(peaks4, x[peaks4], "xk"); plt.plot(x); plt.legend(['threshold'])
# plt.show()