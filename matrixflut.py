import telnetlib
import time
from PIL import Image, ImageDraw, ImageFont

class Client(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.telnet = telnetlib.Telnet(self.host, self.port)

    def sendPixel(self, x, y, rgb):
        message = ("PX {} {} {}\n".format(x, y, rgb)).encode('ascii')
        self.telnet.write(message)

    def close(self):
        self.telnet.close()

    def getSize(self):
        # FIXME currently results in broken pipe
        self.telnet.write("SIZE\n".encode('ascii'))
        io, ix, response = self.telnet.expect([b"SIZE [0-9]* [0-9]*\n"], 3)
        width = int(response.split()[1])
        height = int(response.split()[2])
        return width, height

    def clearMatrix(self):
        #width, height = self.getSize()
        width = 64
        height = 32
        for x in range(width):
            for y in range(height):
                message = ("PX {} {} 000000ff\n".format(x, y)).encode('ascii')
                self.telnet.write(message)

    def sendText(self, text, color=(255, 0, 0), offset=(0, 0), fontfile="spleen-6x12.pil", horizontalCentered=False, verticalCentered=False):
        offsetx, offsety = offset
        size = (64, 32)
        image = Image.new('RGB', size)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load(fontfile)
        (width, height) = font.getsize(text)
        if horizontalCentered:
            x = int((size[0] - width) / 2)
        else:
            x = offsetx
        if verticalCentered:
            y = int((size[1] - height) / 2)
        else:
            y = offsety
        draw.text((x, y), text, fill=color, font=font)
        pixels = image.load()
        for i in range(x, x + width):
            for j in range(y, y + height):
                self.sendPixel(i, j, '%02x%02x%02x' % pixels[i, j])

    def sendImage(self, path, offset=(0, 0), cutout=(0, 0, 0, 0)):
        offsetx, offsety = offset
        image = Image.open(path)
        pixel = image.load()
        width, height = image.size
        for x in range(width):
            for y in range(height):
                r, g, b, alpha = pixel[x, y]
                if alpha != 0:
                    message = ("PX {} {} {}\n".format(x + offsetx, y + offsety, '%02x%02x%02x%02x' % pixel[x, y])).encode('ascii')
                    self.telnet.write(message)

    def sendGIF(self, path, offset=(0, 0), cutout=(0, 0, 0, 0), resize=False):
        frames = self.__processImage(path)
        offsetx, offsety = offset
        cuttop, cutleft, cutwidth, cutheigth = cutout
        while True:
            for f in frames:
                width, height = f.size
                pixel = f.load()
                for x in range(width):
                    for y in range(height):
                        message = ("PX {} {} {}\n".format(x + offsetx, y + offsety, '%02x%02x%02x%02x' % pixel[x, y])).encode('ascii')
                        self.telnet.write(message)
                time.sleep(0.1)


    def __analyseImage(self, path):
        """
        Pre-process pass over the image to determine the mode (full or additive).
        Necessary as assessing single frames isn't reliable. Need to know the mode 
        before processing all frames.
        """
        im = Image.open(path)
        results = {
            'size': im.size,
            'mode': 'full',
        }
        try:
            while True:
                if im.tile:
                    tile = im.tile[0]
                    update_region = tile[1]
                    update_region_dimensions = update_region[2:]
                    if update_region_dimensions != im.size:
                        results['mode'] = 'partial'
                        break
                im.seek(im.tell() + 1)
        except EOFError:
            pass
        return results

    def __processImage(self, path):
        """
        Iterate the GIF, extracting each frame.
        """
        mode = self.__analyseImage(path)['mode']
        
        im = Image.open(path)

        frames = []

        i = 0
        p = im.getpalette()
        last_frame = im.convert('RGBA')
        
        try:
            while True:            
                '''
                If the GIF uses local colour tables, each frame will have its own palette.
                If not, we need to apply the global palette to the new frame.
                '''
                if not im.getpalette():
                    im.putpalette(p)
                
                new_frame = Image.new('RGBA', im.size)
                
                '''
                Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
                If so, we need to construct the new frame by pasting it on top of the preceding frames.
                '''
                if mode == 'partial':
                    new_frame.paste(last_frame)
                
                new_frame.paste(im, (0,0), im.convert('RGBA'))
                frames.append(new_frame.convert('RGBA'))

                i += 1
                last_frame = new_frame
                im.seek(im.tell() + 1)
        except EOFError:
            pass

        return frames


