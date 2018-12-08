import FreeCAD

import numpy as np

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def convertToRGBAArray(RGBint):
    Blue =  RGBint & 255
    Green = (RGBint >> 8) & 255
    Red =   (RGBint >> 16) & 255
    return (Red, Green, Blue, 0xff)

class PixelContainer:
    NUM_COLOR_COMPONENTS = 4

    def __init__(self, resolutionX, resolutionY):
        self.image = Image.new(mode="RGBA", size=(resolutionX, resolutionY))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype("truetype/ttf-bitstream-vera/VeraIt.ttf", 32)
        self.modified = False

    def _colToTup(self, color):
        return (color.r, color.g, color.b, color.a)

    def clear(self, color):
        self.modified = True
        if not color:
            col = (0, 0, 0, 255)
        else:
            col = self._colToTup(color)
        (x,y) = self.image.size
        self.image.paste( (col[0], col[1], col[2], col[3]), [0, 0, x, y] )

    def setPixel_ARGB32(self, pixel):
        self.modified = True
        self.image.putpixel((pixel.pos.x, pixel.pos.y), convertToRGBAArray(pixel.color.argb))

    # interprete subwindow as closed interval on both sides
    def setSubWindowPixels_ARGB32(self, subWindowData):
        self.modified = True
        xmin = min(subWindowData.p1.x, subWindowData.p2.x)
        xmax = max(subWindowData.p1.x, subWindowData.p2.x)
        ymin = min(subWindowData.p1.y, subWindowData.p2.y)
        ymax = max(subWindowData.p1.y, subWindowData.p2.y)

        im = Image.frombuffer("RGBA", (xmax - xmin + 1, ymax - ymin + 1), subWindowData.pixelColor, 'raw', 0, 1)
        self.image.paste(im, (xmin, ymin, xmax, ymax))

    def drawRectangle(self, rectangle):
        self.modified = True
        col = self._colToTup(rectangle.pixelColor)
        fill = None
        if rectangle.filled:
            fill = col
        self.draw.rectangle( [ (rectangle.p1.x, rectangle.p1.y), (rectangle.p2.x, rectangle.p2.y) ], fill = fill, outline = col )

    def drawLine(self, lineData):
        self.modified = True
        col = self._colToTup(lineData.pixelColor)
        self.draw.line([ (lineData.p1.x, lineData.p1.y), (lineData.p2.x, lineData.p2.y) ], fill = col)

    def toString(self):
        return self.image.transpose(Image.FLIP_TOP_BOTTOM).tobytes()

    def setActiveFont(self, fontData):
        try:
            self.font = ImageFont.truetype(fontData.path, fontData.size)
        except IOError:
            FreeCAD.Console.PrintError("Could not open font file: " + fontData.path + "\n")
            self.font = ImageFont.truetype("truetype/ttf-bitstream-vera/VeraIt.ttf", fontData.size)

    def drawText(self, textData):
        self.modified = True
        col = self._colToTup(textData.color)
        self.draw.text((textData.pos.x, textData.pos.y), textData.text, font = self.font, fill=col)

    def getTextSize(self, txt, fontData):
        if fontData.path:
            font = ImageFont.truetype(fontData.path, fontData.size)
            return self.draw.textsize(text = txt, font = font)
        else:
            return self.draw.textsize(text = txt, font = self.font)

    def dirty(self):
        if self.modified:
            self.modified = False
            return True
        return False
