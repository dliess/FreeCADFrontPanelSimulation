import FreeCAD
import FreeCADGui
#from PySide import QtGui
from pivy import coin
from random import randint
import generated.FPSimulation_pb2 as Proto
from array import array


def _findNodeIn(classTypeId, rootNode):
    sa = coin.SoSearchAction()
    sa.setType( classTypeId )
    sa.setSearchingAll(True)
    sa.apply(rootNode)
    if(sa.isFound()):
        return sa.getPath().getTail() 
    else:
        return None

class PixelContainer:
    NUM_COLOR_COMPONENTS = 4

    def __init__(self, resolutionX, resolutionY):
        self.pixelArray = array('B', [0] * PixelContainer.NUM_COLOR_COMPONENTS *
                                      resolutionX * resolutionY)
        self.resolutionX = resolutionX
        self.resolutionY = resolutionY

    def clear(self, color):
        for i in range(self.resolutionX * self.resolutionY):
            self.pixelArray[i+0] = int(color.red   * 255.0)
            self.pixelArray[i+1] = int(color.green * 255.0)
            self.pixelArray[i+2] = int(color.blue  * 255.0)
            self.pixelArray[i+3] =  255

    def setPixel(self, pixel):
        if pixel.pos.x >= self.resolutionX:
            return
        if pixel.pos.y >= self.resolutionY:
            return
        
        i = pixel.pos.y * self.resolutionX * PixelContainer.NUM_COLOR_COMPONENTS \
          + pixel.pos.x * PixelContainer.NUM_COLOR_COMPONENTS

        self.pixelArray[i + 0] = int(pixel.color.red * 255.0)
        self.pixelArray[i + 1] = int(pixel.color.green * 255.0)
        self.pixelArray[i + 2] = int(pixel.color.blue * 255.0)
        self.pixelArray[i + 3] = 255

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
        
        steep = abs(y2 - y1) > abs(x2 - x1);
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1;
        dy = abs(y2 - y1);

        err = dx / 2;

        if y1 < y2:
            ystep = 1;
        else:
            ystep = -1;

        for x in range(x1, x2+1):
            if steep:
                pos = Proto.PixelPos(x = y1, y = x)
            else:
                pos = Proto.PixelPos(x = x, y = y1)
            self.setPixel(Proto.PixelData(pos = pos, color = lineData.pixelColor))
            err -= dy;
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

_pixelContainer = {}

class FPSimDisplay:
    def __init__(self, obj):
        obj.addProperty('App::PropertyInteger', 'ResolutionX').ResolutionX = 10
        obj.addProperty('App::PropertyInteger', 'ResolutionY').ResolutionY = 10
        obj.Proxy = self

    def _reinitTexture(self, obj):
        if _pixelContainer.get(obj.Name):
            del _pixelContainer[obj.Name]
        _pixelContainer[obj.Name] = PixelContainer(obj.ResolutionX, obj.ResolutionY)
        _pixelContainer[obj.Name].clear(Proto.ColorRGB(red = 0, green = 0, blue = 0))
        pixelStr = _pixelContainer[obj.Name].toString()
        resolution = coin.SbVec2s(obj.ResolutionX, obj.ResolutionY)

        for child in obj.Group:
            rootNode = child.ViewObject.RootNode

            # find texture node
            tex = _findNodeIn(coin.SoTexture2.getClassTypeId(), rootNode)
            if not tex:
                FreeCAD.Console.PrintMessage("inserting new texture\n")
                tex =  coin.SoTexture2()
                rootNode.insertChild(tex,1)
            tex.model = coin.SoTexture2.REPLACE
            # create the image for the texture
            image = coin.SoSFImage()
            #FreeCAD.Console.PrintMessage("Initial Texture begin:\n" + self._getTextureString(obj) + "\nTexture End")
            image.setValue(resolution, PixelContainer.NUM_COLOR_COMPONENTS, pixelStr)
            tex.image = image

            # find complexity node
            complexity = _findNodeIn(coin.SoComplexity.getClassTypeId(), rootNode)
            if not complexity:
                FreeCAD.Console.PrintMessage("inserting new complexity\n")
                complexity = coin.SoComplexity()
                rootNode.insertChild(complexity,1)
            complexity.textureQuality = 0.00001

    def _removeTexture(self, obj):
        for child in obj.Group:
            rootNode = child.ViewObject.RootNode
            tex = _findNodeIn(coin.SoTexture2.getClassTypeId(), rootNode)
            if tex:
                rootNode.removeChild(tex)
            complexity = _findNodeIn(coin.SoComplexity.getClassTypeId(), rootNode)
            if complexity:
                rootNode.removeChild(complexity)
    
    def _updateObjectTexture(self, obj):
        pixelContainer = _pixelContainer[obj.Name]
        pixelStr = pixelContainer.toString()
        resolution = coin.SbVec2s(pixelContainer.resolutionX, pixelContainer.resolutionY)
        for child in obj.Group:
            rootNode = child.ViewObject.RootNode
            tex = _findNodeIn(coin.SoTexture2.getClassTypeId(), rootNode)
            image = tex.image 
            image.setValue(resolution, PixelContainer.NUM_COLOR_COMPONENTS, pixelStr)

    def onChanged(self, obj, prop):
        if prop == 'Proxy':
            #newly created
            pass
        elif prop == 'Group':
            # Group modified
            pass
        elif prop == 'ResolutionX':
            if 'ResolutionY' in obj.PropertiesList:
                self._reinitTexture(obj)
        elif prop == 'ResolutionY':
            if 'ResolutionX' in obj.PropertiesList:
                self._reinitTexture(obj)

    def execute(self, obj):
        pass

    def setPixels(self, obj, pixelDataList):
        pixelContainer = _pixelContainer[obj.Name]
        for pixel in pixelDataList.pixelData:
            pixelContainer.setPixel(pixel)
        self._updateObjectTexture(obj)

    def setSubWindowPixels(self, obj, subWindowData):
        pixelContainer = _pixelContainer[obj.Name]
        pixelContainer.setSubWindowPixels(subWindowData)
        self._updateObjectTexture(obj)

    def drawRectangle(self, obj, rectData):
        pixelContainer = _pixelContainer[obj.Name]
        pixelContainer.drawRectangle(rectData)
        self._updateObjectTexture(obj)


    def drawLine(self, obj, lineData):
        pixelContainer = _pixelContainer[obj.Name]
        pixelContainer.drawLine(lineData)
        self._updateObjectTexture(obj)


    def clearDisplay(self, obj, color):
        _pixelContainer[obj.Name].clear(color)
        self._updateObjectTexture(obj)


    def getResolution(self, obj):
        answ = Proto.DisplayResolutionAnswer(x = obj.ResolutionX,
                                             y = obj.ResolutionY)
        return answ

    

class FPSimDisplayViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        import FPSimDir
        return FPSimDir.__dir__ + '/icons/Display.svg'

def createFPSimDisplay():
    obj = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'FPSimDisplay')
    FPSimDisplay(obj)
    FPSimDisplayViewProvider(obj.ViewObject)

    selection = FreeCAD.Gui.Selection.getSelection()
    for selObj in selection:
        obj.addObject(selObj)
    obj.Proxy._reinitTexture(obj)
