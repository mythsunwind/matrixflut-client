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

    client.clearMatrix(offset = (52, 1), width=7, height=7)

    if args.width == 0:
        client.clearMatrix()
    else:
        client.clearMatrix(offset = (args.x, args.y), width=args.width, height=args.height)

    client.close()
