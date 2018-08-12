import FreeCAD
import generated.FPSimulation_pb2 as Proto

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class PixelContainer:
    NUM_COLOR_COMPONENTS = 4

    def __init__(self, resolutionX, resolutionY):
        self.image = Image.new(mode="RGBA", size=(resolutionX, resolutionY))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype("truetype/ttf-bitstream-vera/VeraIt.ttf", 32)

    def _colToTup(self, color):
        return (color.r, color.g, color.b, color.a)

    def clear(self, color):
        if not color:
            col = (0, 0, 0, 255)
        else:
            col = self._colToTup(color)
        (x,y) = self.image.size
        self.image.paste( (col[0], col[1], col[2], col[3]), [0, 0, x, y] )

    def setPixel(self, pixel):
        col = [pixel.color.r, pixel.color.g, pixel.color.b, pixel.color.a]
        self.image.putpixel((pixel.pos.x, pixel.pos.y), (col[0], col[1], col[2], col[3]))

    # interprete subwindow as closed interval on both sides
    def setSubWindowPixels(self, subWindowData):
        xmin = min(subWindowData.p1.x, subWindowData.p2.x)
        xmax = max(subWindowData.p1.x, subWindowData.p2.x)
        ymin = min(subWindowData.p1.y, subWindowData.p2.y)
        ymax = max(subWindowData.p1.y, subWindowData.p2.y)

        pixel = Proto.PixelData()
        pixel.pos.x = xmin
        pixel.pos.y = ymin
        for color in subWindowData.pixelColor:    
            pixel.color = color
            self.setPixel(pixel)
            pixel.pos.x += 1
            if pixel.pos.x > xmax:
                pixel.pos.x = xmin
                pixel.pos.y += 1
                if pixel.pos.y > ymax:
                    return

    def drawRectangle(self, rectangle):
        col = self._colToTup(rectangle.pixelColor)
        fill = None
        if rectangle.filled:
            fill = col
        self.draw.rectangle( [ (rectangle.p1.x, rectangle.p1.y), (rectangle.p2.x, rectangle.p2.y) ], fill = fill, outline = col )

    def drawLine(self, lineData):
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
        col = self._colToTup(textData.color)
        self.draw.text((textData.pos.x, textData.pos.y), textData.text, font = self.font, fill=col)

