import FreeCAD
import numpy as np
import generated.FPSimulation_pb2 as Proto

class PixelContainer:
    NUM_COLOR_COMPONENTS = 4

    def __init__(self, resolutionX, resolutionY):
        self.pixelArray = np.zeros((resolutionY, resolutionX, PixelContainer.NUM_COLOR_COMPONENTS), dtype=np.uint8)
        self.resolutionX = resolutionX
        self.resolutionY = resolutionY

    def clear(self, color):
        for x in range(self.resolutionX):
            for y in range(self.resolutionY):
                self.pixelArray[y,x,0] = int(color.red   * 255.0)
                self.pixelArray[y,x,1] = int(color.green * 255.0)
                self.pixelArray[y,x,2] = int(color.blue  * 255.0)
                self.pixelArray[y,x,3] =  255

    def setPixel(self, pixel):
        if pixel.pos.x >= self.resolutionX:
            return
        if pixel.pos.y >= self.resolutionY:
            return
        
        self.pixelArray[pixel.pos.y, pixel.pos.x, 0] = int(pixel.color.red * 255.0)
        self.pixelArray[pixel.pos.y, pixel.pos.x, 1] = int(pixel.color.green * 255.0)
        self.pixelArray[pixel.pos.y, pixel.pos.x, 2] = int(pixel.color.blue * 255.0)
        self.pixelArray[pixel.pos.y, pixel.pos.x, 3] = 255

    def limitPixelCoord(self, pixelCoord):
        pixelCoord.x = max(pixelCoord.x, 0)
        pixelCoord.x = min(pixelCoord.x, self.resolutionX - 1)
        pixelCoord.y = max(pixelCoord.y, 0)
        pixelCoord.y = min(pixelCoord.y, self.resolutionY - 1)

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
        if rectangle.filled:
            if rectangle.p1.x < rectangle.p2.x:
                arr = range(rectangle.p1.x, rectangle.p2.x + 1)
            else:
                arr = range(rectangle.p2.x, rectangle.p1.x + 1)
            for X in arr:
                p1 = Proto.PixelPos(x = X, y = rectangle.p1.y)
                p2 = Proto.PixelPos(x = X, y = rectangle.p2.y)
                lineData = Proto.LineData(p1 = p1, p2 = p2, pixelColor = rectangle.pixelColor)
                self.drawLine(lineData)
        else:
            p1 = rectangle.p1
            p2 = Proto.PixelPos(x = rectangle.p1.x, y = rectangle.p2.y)
            p3 = rectangle.p2
            p4 = Proto.PixelPos(x = rectangle.p2.x, y = rectangle.p1.y)
            self.drawLine(Proto.LineData(p1 = p1, p2 = p2, pixelColor = rectangle.pixelColor))
            self.drawLine(Proto.LineData(p1 = p2, p2 = p3, pixelColor = rectangle.pixelColor))
            self.drawLine(Proto.LineData(p1 = p3, p2 = p4, pixelColor = rectangle.pixelColor))
            self.drawLine(Proto.LineData(p1 = p4, p2 = p1, pixelColor = rectangle.pixelColor))

    def drawLine(self, lineData):
        # Bresenham's algorithm - thx wikpedia
        x1 = lineData.p1.x
        y1 = lineData.p1.y
        x2 = lineData.p2.x
        y2 = lineData.p2.y
        
        steep = abs(y2 - y1) > abs(x2 - x1)
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = abs(y2 - y1)

        err = dx / 2

        if y1 < y2:
            ystep = 1
        else:
            ystep = -1

        for x in range(x1, x2+1):
            if steep:
                pos = Proto.PixelPos(x = y1, y = x)
            else:
                pos = Proto.PixelPos(x = x, y = y1)
            self.setPixel(Proto.PixelData(pos = pos, color = lineData.pixelColor))
            err -= dy
            if err < 0:
                y1 += ystep
                err += dx

    def toString(self):
        # will interpret array as string
        return self.pixelArray.tostring()

    def dump(self):
        FreeCAD.Console.PrintMessage("PixData:\n")
        for pixelComponent in self.pixelArray:
            FreeCAD.Console.PrintMessage(str(pixelComponent))
        FreeCAD.Console.PrintMessage("PixData END:\n")