from matrixflut import Endpoint, Offset, setPixel, clearMatrix, Pixel
import schedule
import os
import sys
import time

online = False

def checkOnline():
    global online
    response = os.system("/bin/ping -c 1 192.168.178.1")
    if response != 0:
        print("Raspberry pi seems to be offline")
        online = False
        try:
            endpoint = Endpoint("192.168.178.48", "1234")
            setPixel(endpoint, Pixel(53, 2, "ffffff"))
            setPixel(endpoint, Pixel(54, 2, "ffffff"))
            setPixel(endpoint, Pixel(55, 2, "ffffff"))
            setPixel(endpoint, Pixel(56, 2, "ffffff"))
            setPixel(endpoint, Pixel(57, 2, "ff0000"))
            setPixel(endpoint, Pixel(55, 4, "ff0000"))
            setPixel(endpoint, Pixel(54, 4, "ffffff"))
            setPixel(endpoint, Pixel(56, 4, "ffffff"))
            setPixel(endpoint, Pixel(55, 6, "ffffff"))
            setPixel(endpoint, Pixel(58, 1, "ff0000"))
            setPixel(endpoint, Pixel(56, 3, "ff0000"))
            setPixel(endpoint, Pixel(54, 5, "ff0000"))
            setPixel(endpoint, Pixel(53, 6, "ff0000"))
            setPixel(endpoint, Pixel(52, 7, "ff0000"))
        except:
            print("Unexpected error: " + str(sys.exc_info()))
    else:
        # clear matrix once we're online again
        if online == False:
            try:
                endpoint = Endpoint("192.168.178.48", "1234")
                clearMatrix(endpoint, offset = Offset(52, 1), width=7, height=7)
                online = True
            except:
                print("Unexpected error: " + str(sys.exc_info()))


if __name__ == '__main__':
 
     # Schedule offline check
     schedule.every(1).minutes.do(checkOnline)

     while(True):
         schedule.run_pending()
         time.sleep(1)

