import numpy as np

import Logger

class DataManager():

    def initFiles(self):
        self.file_real = open(self.path + "/" + self.file_prefix + "_real.csv", "a")
        self.file_imag = open(self.path + "/" + self.file_prefix + "_imag.csv", "a")

    def writeData(self, real, imag):
        # Check if file was initalized
        if(self.file_real == None or self.file_imag == None):
            Logger.error("You must initalize the files before writing to them.")
            return 

        # Build the strings to write 
        data_real = ""
        for r in range(len(real)):
            data_real += str(real[r])
            if(r != len(real) - 1):
                data_real+=","
        data_real += "\n"

        data_imag = ""
        for i in range(len(imag)):
            data_imag += str(imag[r])
            if(i != len(imag) - 1):
                data_imag+=","
        data_imag += "\n"

        # Append to the files
        self.file_real.write(data_real)
        self.file_imag.write(data_imag)

    def readData(self):
        real = np.genfromtxt(self.path + "/" + self.file_prefix + "_real.csv", delimiter=',')
        imag = np.genfromtxt(self.path + "/" + self.file_prefix + "_imag.csv", delimiter=',')
        
        return np.array([real,imag])

    
    def __init__(self,file_prefix, path="csv"):
       self.file_prefix = file_prefix
       self.path = path
       self.file_real = None
       self.file_imag = None



