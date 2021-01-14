from matrixflut import Client

if __name__ == '__main__':
    client = Client("192.168.178.48", "1234")
    client.clearMatrix()
    client.close()
