from matrixflut import Endpoint, clearMatrix, Offset
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", type=int, default=0)
    parser.add_argument("-y", type=int, default=0)
    parser.add_argument("-width", type=int, default=0)
    parser.add_argument("-height", type=int, default=0)
    args = parser.parse_args()

    endpoint = Endpoint("192.168.178.48", "1234")
    if args.x == 0:
        clearMatrix(endpoint=endpoint)
    else:
        offset = Offset(51, 1)
        clearMatrix(endpoint=endpoint, offset=offset, width=7, height=7)

