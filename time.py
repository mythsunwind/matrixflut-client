from PIL import Image, ImageDraw, ImageFont
from matrixflut import Endpoint, drawText, Offset, setPixel, setBrightness, clearMatrix, Pixel
from datetime import datetime
import os
import sys
import time

class TimeLED:

    def __init__(self):
        self.formerdate = ''
        self.formertext = ''
        self.formerhour = -1
        self.blue = (0, 153, 255)
        self.color = (80, 0, 0)
        self.dyecolor = (255, 0, 0)

    def writeTime(self, text):
        try:
            endpoint = Endpoint("192.168.178.48", "1234")
            drawText(endpoint, text, color=self.color, dyecolor=self.dyecolor, offset=Offset(17, 8), horizontalCentered=True)
        except:
            print("Unexpected error on setting display: " + str(sys.exc_info()))

    def writeDate(self, text):
        try:
            endpoint = Endpoint("192.168.178.48", "1234")
            drawText(endpoint, text, color=self.color, dyecolor=self.dyecolor, offset=Offset(17, 0), fontfile="spleen-5x8.pil", horizontalCentered=True)
        except:
            print("Unexpected error on setting display: " + str(sys.exc_info()))

    def setBrightness(self, brightness):
        try:
            endpoint = Endpoint("192.168.178.48", "1234")
            setBrightness(endpoint, brightness)
        except:
            print("Unexpected error on setting brightness: " + str(sys.exc_info()))

    def clearMatrix(self):
        try:
            endpoint = Endpoint("192.168.178.48", "1234")
            clearMatrix(endpoint)
        except:
            print("Could not clear matrix: " + str(sys.exc_info()))

    def setDate(self, now):
        date = now.strftime("%d %b")
        if self.formerdate != date:
            print(date)
            self.writeDate(date)

        self.formerdate = date

    def setTime(self, now):
        text = now.strftime("%H:%M")
        if self.formertext != text:
            print(text)
            self.writeTime(text)

        self.formertext = text

        if self.formerhour != now.hour:
            if now.hour < 8 or now.hour > 18:
                self.setBrightness(60)
            else:
                self.setBrightness(100)

        self.formerhour = now.hour

if __name__ == '__main__':

    timeLED = TimeLED()
    time.sleep(2)

    while(True):
        timeLED.setTime(datetime.now())
        timeLED.setDate(datetime.now())
        time.sleep(1)

