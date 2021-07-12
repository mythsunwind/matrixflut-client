from matrixflut import Endpoint, Pixel, setPixel
import logging
import sys
import argparse
import urllib.request

log = logging.getLogger('sendImage')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("x", type=int, default=0)
    parser.add_argument("y", type=int, default=0)
    parser.add_argument("rgb")
    args = parser.parse_args()

    try:
        endpoint = Endpoint("192.168.178.48", 1234);
        pixel = Pixel(args.x, args.y, args.rgb)
        setPixel(endpoint, pixel)
    except KeyboardInterrupt:
        log.info("Stopping...")
