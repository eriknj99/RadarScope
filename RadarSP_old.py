import numpy as np
import scipy.fft as fft
import matplotlib as mpl
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
    FFT_mag = cleanData(FFT_mag, fft_size)
    # Get just the first half of FFT matrix
    FFT_mag = splitData(FFT_mag, fft_size)
    # Filter out clutter and/or noise
    
    # Remove low frequency components from FFT_mat
#    FFT_mat = filterLowData(FFT_mag)
    
    # Complete range calculations
    R = range(fft_size, sample_rate, FFT_mag)
    
    # Complete Speed Calculations
    S = speed(fft_size, sample_rate, FFT_mag)
    
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
def range(fft_size, sample_rate, FFT_mat):    
    # Calculate range weights
    #   Convert noise reduced fft magnitudes to dBv 
    R = dBv(FFT_mat[0,:]-FFT_mat[1,:])
    
    #x = np.linspace(0,fft_size)
    #y = x

    #R = R * y

    # R = c*t/2 where t = fr/(B*2/T) so R = fr*c*T/(B*4)
    # R is range, c is speed of light, t is time for signal to travel to and return from target
    # fr is return frequency, B is bandwidth, T is modulation period (Up and Down chirp time
    # Return range array
    return R


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
    Sinit = fft.fft(FFT_mat[0],N)
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
    

# Turns all frequency components below some frequency value to 1's
#def filterLowData(FFT_recent):
#    # create array with all ones same size as FFT_recent
#    NoLow = np.ones(np.shape(FFT_recent))
#    NoLow[frArray > fmin] = FFT_recent[frArray > fmin]
#    return NoLow
    

    

    
    
