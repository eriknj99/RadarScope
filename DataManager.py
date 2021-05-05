import numpy as np

import Logger

path = "csv"
file_real = None
file_imag = None

def initFile(file_prefix):
    file_real = open(path + "/" + file_prefix + "_real.csv", "a")
    file_imag = open(path + "/" + file_prefix + "_imag.csv", "a")

def writeData(file_prefix, real, imag):
    # Check if file was initalized
    if(file_real == None or file_imag == None):
        Logger.error("You must initalize the files before writing to them.")
        return 

    # Build the strings to write 
    data_real = ""
    for r in range(real):
        data_real += real[r]
        if(r != len(real) - 1):
            data_real+=","
    data_real += "\n"

    data_imag = ""
    for i in range(imag):
        data_imag += imag[r]
        if(i != len(imag) - 1):
            data_imag+=","
    data_imag += "\n"

    # Append to the files
    file_real.write(data_real)
    file_imag.write(data_imag)
    

def readData(file_prefix):
    real = np.genfromtxt(path + "/" + file_prefix + "_real.csv", delimiter=',')
    imag = np.genfromtxt(path + "/" + file_prefix + "_imag.csv", delimiter=',')
    
    return np.array([real,imag])


