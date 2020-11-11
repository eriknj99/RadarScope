from time import sleep
import time
import numpy
import math
import serial
import numpy as np
import random
import matplotlib.pyplot as plt
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import io
from matplotlib.pyplot import figure

# Initialize the pygame display with a resizable window
def initDisplay():
    pygame.init()
    white = (255, 255, 255)
    X = 1000
    Y = 500
    display_surface = pygame.display.set_mode((X, Y ),pygame.RESIZABLE)
    pygame.display.set_caption('floatme')
    return display_surface

# Set custom colors
bgColor = "#000000"
fgColor = "#00FF00"
pltColor = "#00FF00"

# Set Serial Port
serialPort = "/dev/ttyACM0"

# Statustext
statusTxt = ""

connect = True # Set this to false for debugging without access to serial data, Random Data will be used 


if connect:
    try:
        ser = serial.Serial(serialPort, 115200)
        statusTxt = " CONNECTED " + serialPorty
    except:
        #If a connection could not be established set connect to false and set plot color to red
        connect = False
        pltColor = "#FF0000"
        print("Error: Unable to establish serial connection to " + serialPort)
        statusTxt = " DISCONNECTED"

display_surface = initDisplay()
font = pygame.font.SysFont("Monospace", 20)

figure(figsize=(10,5))

# Set dark background color
plt.style.use('dark_background')

time_holder = time.time()
# Main Loop
while True:
    #Read in raw serial data.
    #If port is disconnected set mode to disconnected
    #If port is reconnected set mode back to connected 
    #This should allow hotplugging
    if connect:
            try:
                raw = str(ser.readline()).replace("\\r\\n", "")
                statusTxt = " CONNECTED " + serialPort
            except:
                connect = False
                pltColor = "#FF0000"
                print("Error: Unable to establish serial connection to " + serialPort)
                statusTxt = " DISCONNECTED"
                raw = ""
                for i in range(0,2048):
                    raw += (str( max(0,((random.random() * 100) - 90)) ))
                    raw += (" ")
    else:
        try:
            ser = serial.Serial(serialPort, 115200)
            statusTxt = " CONNECTED " + serialPort
        except:
            statusTxt = " DISCONNECTED"
            raw = ""
            for i in range(0,2048):
                raw += "0.0"
                raw += (" ")


    #Process raw data into 2 float arrays
    rawList = raw.rsplit(" ")
    datax = []
    datay = []
    count = 0.0
    for vs in rawList:
        try:
            datay.append(float(vs))
            datax.append(count)
            count+=1.0
        except ValueError:
            pass

    #Plot the data
    plt.plot(datax,datay,color=pltColor)
    plt.title("Radar Scope")

    #Set custom styling 
    plt.grid(color=fgColor, linestyle=':', linewidth=1)
    ax = plt.gca()
    ax.set_facecolor(bgColor)
    ax.spines['bottom'].set_color(fgColor)
    ax.spines['top'].set_color(fgColor)
    ax.spines['right'].set_color(fgColor)
    ax.spines['left'].set_color(fgColor)
    ax.yaxis.label.set_color(fgColor)
    ax.xaxis.label.set_color(fgColor)
    ax.title.set_color(fgColor)

    #Save plot image to a buffer
    buf = io.BytesIO()
    plt.savefig(buf)

    #Load buffer into pygame image
    buf.seek(0)
    image = pygame.image.load(buf) 



    # Draw the plot image on screen
    display_surface.blit(image, (0, 0))


    #Calculate refresh rate and draw status on screen
    statusTxt += "    refresh: " + str((round(1/(time.time() - time_holder), 2))) + "Hz" 
    time_holder = time.time()
    status = font.render(statusTxt, True, pltColor)
    display_surface.blit(status, (0, 0))

    #Update the display
    pygame.display.update()

    #Clear the plot so that only one set of data is displayed at a time
    plt.clf()

    # Handle pygame events (Do nothing )
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            quit()

