import numpy as np
import scipy.fft as fft
import matplotlib as mpl



# Import MATLAB table with constants fitted for scaling function
from scipy.io import loadmat
x = loadmat('beta_n4.mat.old')
beta = loadmat('beta_n4.mat.old')['beta']

# number of degrees for poly solve
n = 4.
# Create array of powers 
p = np.arange(0., n+1)

#import csv

# with open('output_JackWalk.csv') as datafile:
    # data = csv.reader(datafile)
    # for row in data:
        # print(', '.join(row))
# Set necessary constant values
B = 100e6
c = 3e8
fc = 2.45e9
T = 8.7e-3 

# Create scale that multiplies frequency return to give range
scale = c*T/(B*4);

# Calculate Wavelength
lam = c/fc
    
Rmin = 3 # Set minimum range to 3m
fmin = Rmin/scale # Find corresponding frequency

# Create array ranging from 0 to half the sample_rate
# with number of steps being half the fft_size
#frArray = np.linspace(0, sample_rate/2, fft_size/2)

# Range array based on return frequency
#RArray = np.multiply(frArray, scale)

# Create copy of return frequency array
#frHigh = frArray
# Zero out all frequencies below the desired minimum
#frHigh[frHigh < fmin] = 0
        

def SP(fft_size, sample_rate, FFT_mag, FFT_real, FFT_imag):
    # Combine real and imaginart partd of data
    FFT_mat = FFT_real + 1j*FFT_imag
    # Clean FFT data - Combine real & imag, Split in half, Noise Reduction
    # FFT_mag = cleanData(FFT_mag, fft_size)
    # Get just the first half of FFT matrix
    FFT_mag = splitData(FFT_mag, fft_size)
    
    # Remove low frequency components from FFT_mat
    #FFT_mat = filterLowData(FFT_mag)
    
    # Complete range calculations
    R = getRange(fft_size, sample_rate, FFT_mag)
    
    # Complete Speed Calculations
    S = speed(fft_size, sample_rate, FFT_mat)
    
    # Return 2 by fft_size/2 array - First row is range data - Second row is speed data
    return np.hstack((R,S))


# Split the data and reduce noise 
def cleanData(FFT_mat, fft_size):
    FFT_mat = splitData(FFT_mat, fft_size)
    FFT_mat = noiseRed(FFT_mat)
    return FFT_mat


# Returns just the first half of the data, second half is a copy    
def splitData(FFT_mat, fft_size):
    # Return just the first half of the columns of the data, ignore the duplicated area
    return FFT_mat[:,:int(fft_size/2)]
 
 
# Reduces noise throught all frequencies and fft instances
def noiseRed(FFT_mat):
    return FFT_mat


# Recieves size of the FFT computed, ADC sample rate, and the matrix containing FFT 
# Returns 1-D range array containing weight values for each distance
def getRange(fft_size, sample_rate, FFT_mat):    
    # Calculate range weights
    #   Subtract previous FFT magnitudes from current to get range weights for moving targets
    R = np.absolute(FFT_mat[0,:]-FFT_mat[1,:])
    
    # Scale the weights contained in R to increase detection range, reduce noise 
    Rscaled = scaleR(R)
    
    # R = c*t/2 where t = fr/(B*2/T) so R = fr*c*T/(B*4)
    # R is range, c is speed of light, t is time for signal to travel to and return from target
    # fr is return frequency, B is bandwidth, T is modulation period (Up and Down chirp time
    
    # Return sccaled range array weighted in dBv elements in (-inf, 40]
    #return dBv(R)
    
    # Return elements in (0, 100]
    return Rscaled

def scaleR(A):
    scaled = np.zeros(np.size(A))
    for ii in range(np.size(A)):
        item = A[ii]
        val = expFit(ii)
        
        if item > val:
            scaled[ii] = 100
        else: 
            scaled[ii] = 100*(item/val)**2
    return scaled


def expFit(x):
    return np.exp((x**p)@beta)
    
def polyfit(x):
    return x

# Recieves size of the FFT computed, ADC sample rate, and the matrix containing FFT 
def speed(fft_size, sample_rate, FFT_mat):
    # Calculate doppler
    
    # Doppler frequency - fd - half the absolute value of difference between two consecutive return frequencies for same target
    # 
    # Algorithm:
    #   Apply detection of targets
    #   Implement window around target center frequency
    #   Calculate actual frequency for consecutive chirps
    #   Find doppler for the consecutive returns
    #   Get weight of speeds at 
    N = 2**15
    Sinit = fft.fft(FFT_mat[0:1024],N)
    S = dBv(Sinit)
    S = S[0:int(np.size(S)/2)]
    fd = np.linspace(0, int(sample_rate/4), np.size(S))
    maxV = 10; # m/s
    fmax = maxV/lam
    # Return speed Data
    
    return S[fd <= fmax]


# Recieves array of linear values, converts all to dBv and returns array of same size
def dBv(linVal):
    return 20*np.log(np.absolute(linVal))
    

    

    

    
    
