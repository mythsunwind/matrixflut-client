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
        self.online = True

    def writeCenteredText(self, text):
        try:
            client = Client("192.168.178.48", "1234")
            client.sendText(text, color=self.color, horizontalCentered=True, verticalCentered=True)
            client.close()
        except:
            print("Unexpected error on setting display: " + str(sys.exc_info()))

    def clearMatrix(self):
        try:
            client = Client("192.168.178.48", "1234")
            client.clearMatrix()
            client.close()
        except:
            print("Could not clear matrix: " + str(sys.exc_info()))

    def setLED(self, now):
        date = now.strftime("%a %-d.%-m.%Y")
        text = now.strftime("%H:%M")
        if self.formertext != text:
            print(text)
            try:
                self.writeCenteredText(text)
            except:
                self.writeCenteredText("Cannot set time")

        self.formertext = text
		
        """
        if self.formerdate != date:
            print(date)
            try:
                blue = graphics.Color(0, 0, 255)
                # TODO: Only clear date row
                graphics.DrawText(display, font, 8, 10, blue, date)
            except:
                print("Unexpected error on setting date")
                blue = graphics.Color(0, 0, 255)
                # TODO: Only clear date row
                graphics.DrawText(display, font, 8, 10, blue, "Cannot set date")

        self.formerdate = date
        """

        if self.formerhour != now.hour:
            if now.hour < 8 or now.hour > 18:
                self.color = (180, 0, 0)
            else:
                self.color = (255, 0, 0)

        self.formerhour = now.hour

    def checkOnline(self):
        response = os.system("/bin/ping -c 1 192.168.178.1")
        if response != 0:
            print("Raspberry pi seems to be offline")
            self.online = False
            self.writeCenteredText("Offline")
        else:
            # clear matrix once we're online again
            if self.online == False:
                self.online = True
                self.writeCenteredText("       ")

if __name__ == '__main__':

    timeLED = TimeLED()
    timeLED.clearMatrix()

    # Schedule offline check
    schedule.every(1).minutes.do(timeLED.checkOnline)

    while(True):
        timeLED.setLED(datetime.now())
        schedule.run_pending()
        time.sleep(1)

