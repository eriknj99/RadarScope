from termcolor import colored

info_enable = True
debug_enable = True 
error_enable = True

def info(val):
    if(info_enable):
        print(colored("INFO: ", "green") + str(val))

def debug(val):
    if(debug_enable):
        print(colored("DEBUG: ", "blue") + str(val))

def error(val):
    if(error_enable):
        print(colored("ERROR: ", "red") + str(val))
