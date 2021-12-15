from os.path import join
from scipy.io.wavfile import read
import numpy as np
import frame
import ste

FILE_PATH_THHL = 'D:\Documents\XLTHS\Thi CK\TinHieuHuanLuyen'
FILE_WAV_THHL = ['01MDA.wav', '02FVA.wav', '03MAB.wav', '06FTB.wav']
FILE_LAB_THHL = ['01MDA.lab', '02FVA.lab', '03MAB.lab', '06FTB.lab']

INDEX = 0
TIME_FRAME = 0.03

def readFileInput(fileName):
    inputFile = []
    with open(join(FILE_PATH_THHL, fileName)) as file:
        for line in file:
            inputFile.append(line.split())
    for i in range(0, len(inputFile) - 2):
        inputFile[i][0] = int(float(inputFile[i][0]) * frequency / 1323 * 3)
        inputFile[i][1] = int(float(inputFile[i][1]) * frequency / 1323 * 3)
    
    inputFile = inputFile[:-2]
    return inputFile
  
def calThreshold(fileLab, STEArray):
  f = []
  g = []
  index = 0
  for j in range(len(STEArray)):
    if j >= fileLab[index][0] and j < fileLab[index][1]:
      if fileLab[index][2] == 'sil':
        g.append(STEArray[j])
      else:
        f.append(STEArray[j])
    else:
      index += 1
  Tmin = max(g)
  Tmax = min(f)
  T = (Tmin + Tmax) / 2
  tempF = tempG = -1
  countF = countG = 0
    
  for value in f:
    countF += 1 if value > T else 0
  for value in g:
    countG += 1 if value < T else 0
    
  while tempF != countF or tempG != countG:
    avgF = 0
    avgG = 0
    
    for value in f:
      avgF += max(value - T, 0)
    avgF /= len(f)
    for value in g:
      avgG += max(T - value, 0)
    avgG /= len(g)
    
    if (avgF - avgG) > 0:
      Tmin = T
    else:
      Tmax = T
      
    T = (Tmin + Tmax) / 2
    tempF = countF
    tempG = countG
    countF = countG = 0
    
    for value in f:
      countF += 1 if value > T else 0
    for value in g:
      countG += 1 if value < T else 0
      
  return T

# Main
thresholdsArray = np.array([])

for i in range(0, len(FILE_WAV_THHL)):
  frequency, signal = read(join(FILE_PATH_THHL, FILE_WAV_THHL[i]))  
  signal = signal / max(np.max(signal), abs(np.min(signal)))
  frameLength = int(TIME_FRAME * frequency) # Độ dài của 1 frame (đơn vị mẫu)
  framesArray = frame.getFramesArray(signal, frameLength)
  STEArray = ste.calSTE(framesArray)
  fileLab = readFileInput(FILE_LAB_THHL[i])
  T = calThreshold(fileLab, STEArray)
  thresholdsArray = np.append(thresholdsArray, T)
  
print(thresholdsArray)
print(f"Threshold = {np.average(thresholdsArray)}")