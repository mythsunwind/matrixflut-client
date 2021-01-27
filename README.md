# matrixflut-client

Client to send text, images or just individual pixels via Pixelflut protocol

## Usage

Add import in your project:

`from matrixflut import Endpoint, drawText`

Draw red text on center of panel via pixelflut protocol:

```
endpoint = Endpoint("192.168.0.1", "1337")
drawText(endpoint, "Hello", color=(255, 0, 0), horizontalCentered=True, verticalCentered=True)
```

Available client features:

* clearMatrix
* getSize
* setPixel
* setBrightness
* drawText
* drawImage
* drawGIF

## Examples

This repository contains certain example scripts that use the client.

## Licenses

Font [Spleen](https://github.com/fcambus/spleen) is released under the [BSD 2-Clause license](https://github.com/fcambus/spleen/blob/master/LICENSE) by Frederic Cambus.

Gif sending code is inspired and copied from poemusica's [rpi-matrix-gif](https://github.com/poemusica/rpi-matrix-gif) and from BigglesZX's [github gist](https://gist.github.com/BigglesZX/4016539). Thank you!

