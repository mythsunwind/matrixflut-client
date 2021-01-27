from matrixflut import Endpoint, drawText, Offset
import logging
import sys
import argparse
import urllib.request

log = logging.getLogger('sendImage')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("-x", "--offsetx", type=int, default=0)
    parser.add_argument("-y", "--offsety", type=int, default=0)
    args = parser.parse_args()

    endpoint = Endpoint("192.168.178.48", "1234")
    offset = Offset(args.offsetx, args.offsety)
    drawText(endpoint=endpoint, text=args.text, color=(30,30,30), offset=offset, fontfile="spleen-5x8.pil", horizontalCentered=True)

