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
    parser.add_argument("-c", "--color", type=str, default="ff0000")
    parser.add_argument("-d", "--dyecolor", type=str, default=None)
    args = parser.parse_args()

    endpoint = Endpoint("192.168.178.48", "1234")
    offset = Offset(args.offsetx, args.offsety)
    color = tuple(int(args.color[i:i+2], 16) for i in (0, 2, 4))
    if args.dyecolor != None:
        dyecolor = tuple(int(args.dyecolor[i:i+2], 16) for i in (0, 2, 4))
    else:
        dyecolor = None
    drawText(endpoint=endpoint, text=args.text, color=color, dyecolor=dyecolor, offset=offset, fontfile="spleen-5x8.pil", horizontalCentered=True)

