import numpy as np

path = "csv"

def initFile():
    print("TODO")

def writeData(file_prefix, real, imag):
   print("TODO") 

def readData(file_prefix):
    real = np.genfromtxt(path + "/" + file_prefix + "_real.csv", delimiter=',')
    imag = np.genfromtxt(path + "/" + file_prefix + "_imag.csv", delimiter=',')
    
    return np.array([real,imag])


