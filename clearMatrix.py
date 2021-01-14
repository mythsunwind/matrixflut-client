from matrixflut import Client
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", type=int, default=0)
    parser.add_argument("-y", type=int, default=0)
    parser.add_argument("-width", type=int, default=0)
    parser.add_argument("-height", type=int, default=0)
    args = parser.parse_args()

    client = Client("192.168.178.48", "1234")

    if args.width == 0:
        client.clearMatrix()
    else:
        for x in range(args.x, args.x + args.width):
            for y in range(args.y, args.y + args.height):
                client.sendPixel(x, y, "000000ff")

    client.close()
