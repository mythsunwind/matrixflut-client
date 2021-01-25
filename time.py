from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from matrixflut import Client
import schedule
import os
import sys
import time

size = (64, 32)

class TimeLED:

    def __init__(self):
        self.formerdate = ''
        self.formertext = ''
        self.formerhour = -1
        self.color = (255, 0, 0)
        self.datecolor = (30, 30, 30)
        self.online = True

    def writeCenteredText(self, text):
        try:
            client = Client("192.168.178.48", "1234")
            client.sendText(text, color=self.color, horizontalCentered=True, verticalCentered=True)
            client.close()
        except:
            print("Unexpected error on setting display: " + str(sys.exc_info()))

    def writeBottomText(self, text):
        try:
            client = Client("192.168.178.48", "1234")
            client.sendText(text, color=self.datecolor, offset=(0, 23), fontfile="spleen-5x8.pil", horizontalCentered=True)
            client.close()
        except:
            print("Unexpected error on setting display: " + str(sys.exc_info()))

    def setBrightness(self, brightness):
        try:
            client = Client("192.168.178.48", "1234")
            client.setBrightness(brightness)
            client.close()
        except:
            print("Unexpected error on setting brightness: " + str(sys.exc_info()))

    def clearMatrix(self):
        try:
            client = Client("192.168.178.48", "1234")
            client.clearMatrix()
            client.close()
        except:
            print("Could not clear matrix: " + str(sys.exc_info()))

    def setDate(self, now):
        date = now.strftime("%d %b")
        if self.formerdate != date:
            print(date)
            self.writeBottomText(date)

        self.formerdate = date

    def setTime(self, now):
        text = now.strftime("%H:%M")
        if self.formertext != text:
            print(text)
            try:
                self.writeCenteredText(text)
            except:
                self.writeCenteredText("Cannot set time")

        self.formertext = text
		
        if self.formerhour != now.hour:
            if now.hour < 8 or now.hour > 18:
                self.setBrightness(60)
            else:
                self.setBrightness(100)

        self.formerhour = now.hour

    def checkOnline(self):
        response = os.system("/bin/ping -c 1 192.168.178.1")
        if response != 0:
            print("Raspberry pi seems to be offline")
            self.online = False
            self.sendPixel(53, 2, "ffffff")
            self.sendPixel(54, 2, "ffffff")
            self.sendPixel(55, 2, "ffffff")
            self.sendPixel(56, 2, "ffffff")
            self.sendPixel(57, 2, "ff0000")
            self.sendPixel(55, 4, "ff0000")
            self.sendPixel(54, 4, "ffffff")
            self.sendPixel(56, 4, "ffffff")
            self.sendPixel(55, 6, "ffffff")
            self.sendPixel(58, 1, "ff0000")
            self.sendPixel(56, 3, "ff0000")
            self.sendPixel(54, 5, "ff0000")
            self.sendPixel(53, 6, "ff0000")
            self.sendPixel(52, 7, "ff0000")
        else:
            # clear matrix once we're online again
            if self.online == False:
                self.clearMatrix(offset = (52, 1), width=7, height=7)
                self.online = True

if __name__ == '__main__':

    timeLED = TimeLED()
    timeLED.clearMatrix()
    time.sleep(2)

    # Schedule offline check
    schedule.every(1).minutes.do(timeLED.checkOnline)

    while(True):
        timeLED.setTime(datetime.now())
        timeLED.setDate(datetime.now())
        schedule.run_pending()
        time.sleep(1)

