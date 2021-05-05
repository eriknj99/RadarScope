info_enable = True
debug_enable = True 


def info(val):
    if(info_enable):
        print("INFO: " + str(val))

def debug(val):
    if(debug_enable):
        print("DEBUG: " + str(val))
