from matrixflut import Client
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

    try:
        client = Client("192.168.178.48", "1234")
        client.sendText(args.text, color=(30,30,30), offset=(args.offsetx, args.offsety), fontfile="spleen-5x8.pil", horizontalCentered=True)
        client.close()

    except KeyboardInterrupt:
        log.info("Stopping...")
    finally:
        client.close()
