from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from matrixflut import Endpoint, drawText, Offset, clearMatrix
import requests
import logging
import time
import sys

log = logging.getLogger('bitcoin')

def getValueFromApi():
    response = requests.get('https://bitcoinapi.de/widget/current-btc-price/rate.json')
    json = response.json()
    return json['price_eur'].split(',')[0].encode('ascii', 'ignore')

if __name__ == '__main__':

    try:
        endpoint = Endpoint("192.168.178.48", "1234")

        while(True):
            try:
                rate = getValueFromApi()
                drawText(endpoint=endpoint, text=rate, color=(247, 147, 26), offset=Offset(17, 19), horizontalCentered=True, fontfile="spleen-5x8.pil")
            except:
                log.error("Unexpected error on setting display: " + str(sys.exc_info()))
            time.sleep(60 * 15)

    except KeyboardInterrupt:
        log.info("Stopping...")
