from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
import telnetlib
import time

@dataclass
class Endpoint:
    host: str
    port: int

@dataclass
class Pixel:
    x: int
    y: int
    rgb: str

@dataclass
class Offset:
    x: int
    y: int

@dataclass
class Cutout:
    x: int
    y: int
    w: int
    h: int

def setPixel(endpoint: Endpoint, pixel: Pixel):
    telnet = telnetlib.Telnet(endpoint.host, endpoint.port)
    message = ("PX {} {} {}\n".format(pixel.x, pixel.y, pixel.rgb)).encode('ascii')
    telnet.write(message)
    telnet.close()

def getSize(endpoint: Endpoint):
    telnet = telnetlib.Telnet(endpoint.host, endpoint.port)
    telnet.write("SIZE\n".encode('ascii'))
    io, ix, response = telnet.expect([b"SIZE [0-9]* [0-9]*\n"], 3)
    width = int(response.split()[1])
    height = int(response.split()[2])
    telnet.close()
    return width, height

def setBrightness(endpoint: Endpoint, brightness: int):
    telnet = telnetlib.Telnet(endpoint.host, endpoint.port)
    message = ("BRIGHTNESS {}\n".format(brightness)).encode('ascii')
    telnet.write(message)
    telnet.close()

def clearMatrix(endpoint: Endpoint, offset=Offset(0, 0), width = 64, height = 32):
    #width, height = getSize(endpoint)
    telnet = telnetlib.Telnet(endpoint.host, endpoint.port)
    for x in range(0 + offset.x, width + offset.x):
        for y in range(0 + offset.y, height + offset.y):
            message = ("PX {} {} 000000ff\n".format(x, y)).encode('ascii')
            telnet.write(message)
    telnet.close()

def drawText(endpoint: Endpoint, text: str, color=(255, 0, 0), offset=Offset(0, 0), fontfile="spleen-6x12.pil", horizontalCentered=False, verticalCentered=False, dyecolor=None):
    size = (64, 32)
    image = Image.new('RGB', size)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load(fontfile)
    (width, height) = font.getsize(text)
    if horizontalCentered:
        x = int((size[0] - width) / 2)
    else:
        x = offset.x
    if verticalCentered:
        y = int((size[1] - height) / 2)
    else:
        y = offset.y
    draw.text((x, y), text, fill=color, font=font)
    pixels = image.load()
    if dyecolor != None:
        for k in range(x, x + width):
            for l in range(y, y + int(height / 3) + 1):
                if pixels[k, l] != (0, 0, 0):
                    print("{},{}".format(k, l))
                    pixels[k, l] = dyecolor
    telnet = telnetlib.Telnet(endpoint.host, endpoint.port)
    for i in range(x, x + width):
        for j in range(y, y + height):
            message = ("PX {} {} {}\n".format(i, j, '%02x%02x%02x' % pixels[i, j])).encode('ascii')
            telnet.write(message)
    telnet.close()

def drawImage(endpoint: Endpoint, path: str, offset=Offset(0, 0), cutout=Cutout(0, 0, 0, 0)):
    image = Image.open(path)
    pixel = image.load()
    width, height = image.size
    telnet = telnetlib.Telnet(endpoint.host, endpoint.port)
    for x in range(width):
        for y in range(height):
            r, g, b, alpha = pixel[x, y]
            if alpha != 0:
                message = ("PX {} {} {}\n".format(x + offset.x, y + offset.y, '%02x%02x%02x%02x' % pixel[x, y])).encode('ascii')
                telnet.write(message)
    telnet.close()

def drawGIF(endpoint: Endpoint, path: str, offset=Offset(0, 0), cutout=Cutout(0, 0, 0, 0), resize=False):
    frames = __processImage(path)
    # TODO: cutout
    telnet = telnetlib.Telnet(endpoint.host, endpoint.port)
    try:
        while True:
            for f in frames:
                width, height = f.size
                pixel = f.load()
                for x in range(width):
                    for y in range(height):
                        message = ("PX {} {} {}\n".format(x + offset.x, y + offset.y, '%02x%02x%02x%02x' % pixel[x, y])).encode('ascii')
                        telnet.write(message)
                time.sleep(0.1)
    finally:
        telnet.close()

def __analyseImage(path):
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

def __processImage(path):
    """
    Iterate the GIF, extracting each frame.
    """
    mode = __analyseImage(path)['mode']
    
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


