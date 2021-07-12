from matrixflut import Endpoint, drawImage, Offset
import logging
import sys
import argparse
import urllib.request

log = logging.getLogger('sendImage')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("-x", "--offsetx", type=int, default=0)
    parser.add_argument("-y", "--offsety", type=int, default=0)
    args = parser.parse_args()

    if args.path.find("http") != -1:
        with urllib.request.urlopen(args.path) as url:
            with open('temp.png', 'wb') as f:
                f.write(url.read())
                args.path = 'temp.png'

    try:
        endpoint = Endpoint("192.168.178.48", "1234")
        drawImage(endpoint=endpoint, path=args.path, offset=Offset(args.offsetx, args.offsety))
    except:
        log.info("Stopping...")
