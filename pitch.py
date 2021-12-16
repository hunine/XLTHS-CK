from scipy.signal import find_peaks
import numpy as np

def getPitch(index, frequency, framesArray, frameLength, markPoint):
  hamming = np.hamming(frameLength)
  if (markPoint[index] == 1):
    frame = framesArray[index] * hamming
    spectrum = abs(np.fft.fft(frame, 2 ** 13))[:2 ** 12]
    peaks, _  = find_peaks(spectrum, distance=10, prominence=8.5)
    fs = np.linspace(0, frequency / 2, len(spectrum))
    if len(peaks) >= 3:
      l1 = abs(fs[peaks[0]] - fs[peaks[1]])
      l2 = abs(fs[peaks[1]] - fs[peaks[2]])
      if l1 > 70 and l1 < 400 and l2 > 70 and l2 < 400:
        times = l1 / l2
        if times > 1.5 or 1 / times > 1.5:
          return min(l1, l2)
        return (l1 + l2) / 2
    elif len(peaks) == 2:
      l = abs(fs[peaks[0]] - fs[peaks[1]])
      if l > 70 and l < 400:
        return l
  return 0   