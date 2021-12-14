import numpy as np

# Hàm tính STE
def calSTE(framesArray):
  ste = np.zeros(len(framesArray))
  
  for i in range(len(framesArray)):
    ste[i] = np.sum(framesArray[i]**2)
  ste = ste / np.max(ste)
  
  return ste

# Phân biệt đoạn tiếng nói và đoạn khoảng lặng
def findSpeechAndSilence(STEArray, threshold = 0.0584):
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