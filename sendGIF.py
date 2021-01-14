from matrixflut import Client
import sys
import argparse
import urllib.request

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
#    parser.add_argument("host")
#    parser.add_argument("port", type=int)
    parser.add_argument("path")

    parser.add_argument("-x", "--offsetx", type=int, default=0)
    parser.add_argument("-y", "--offsety", type=int, default=0)

    args = parser.parse_args()

    if args.path.find("http") != -1:
        with urllib.request.urlopen(args.path) as url:
            with open('temp.jpg', 'wb') as f:
                f.write(url.read())
                args.path = 'temp.jpg'

    client = Client("192.168.178.48", "1234")
    client.sendGIF(args.path, (args.offsetx, args.offsety), resize=True)
    client.close()
