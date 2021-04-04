import AsyncSerialInput

# Initialize the Serial Input
ds = AsyncSerialInput.AsyncSerialInput()

f = open("output.csv", "a")
count = 0
while(True):
    fft = ds.getNext()
    line = ""
    for i in fft:
        line += str(i) + ","
    f.write(line + "\n")
    count+=1
    print("Saved " + str(count) + " FFTs", end="\r")

f.close()


