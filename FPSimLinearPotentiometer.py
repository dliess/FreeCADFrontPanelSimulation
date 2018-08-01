import FreeCAD
import FreeCADGui
import FPEventDispatcher
from FPInitialPlacement import InitialPlacements
import FPSimServer
import FPUtils

pressEventLocationXY = dict()
offsetDistanceAtPress = dict()

class FPSimLinearPotentiometer(InitialPlacements):
    def __init__(self, obj):
        InitialPlacements.__init__(self, obj)
        pressEventLocationXY[obj.Name] = []
        offsetDistanceAtPress[obj.Name] = 0
        obj.addProperty('App::PropertyPythonObject', 'OffsetDistance').OffsetDistance = 0
        obj.addProperty('App::PropertyFloat', 'NegativeDistLimit').NegativeDistLimit = 25
        obj.addProperty('App::PropertyFloat', 'PositiveDistLimit').PositiveDistLimit = 25
        obj.addProperty('App::PropertyVector', 'PositiveDirection').PositiveDirection = (0,0,1)
        obj.addProperty('App::PropertyInteger', 'Resolution').Resolution = 1024
        obj.addProperty('App::PropertyInteger', 'NumSnapInPositions').NumSnapInPositions = 0 #TODO: implement

        obj.Proxy = self

    def _registerEventCallbacks(self, objName):
        FPEventDispatcher.eventDispatcher.registerForButtonEvent(objName, self.onButtonEvent)

    def _unregisterEventCallbacks(self, objName):
        FPEventDispatcher.eventDispatcher.unregisterForButtonEvent(objName)

    def onChanged(self, obj, prop):
        if prop == 'Proxy':
            self._registerEventCallbacks(obj.Name)
            FPSimServer.dataAquisitionCBHolder.setPotentiometerCB(obj.Name, self.getValue)
        elif prop == 'Group':
            if not obj.Group:
                self._unregisterEventCallbacks(obj.Name)
                FPSimServer.dataAquisitionCBHolder.clearPotentiometerCB(obj.Name)
                offsetDistanceAtPress[obj.Name] = 0
            elif self.hasNoChilds(obj):
                self._registerEventCallbacks(obj.Name)
                FPSimServer.dataAquisitionCBHolder.setPotentiometerCB(obj.Name, self.getValue)
            self.saveInitialPlacements(obj) 
        elif prop == 'ExpressionEngine':
            try:
                obj.OffsetDistance = 0
                self.moveToInitialPlacement(obj)
            except KeyError:
                self.saveInitialPlacements(obj)


    def execute(self, obj):
        pass
        #FreeCAD.Console.PrintMessage("execute " + obj.Name + "\n")

    def onButtonEvent(self, objName, state, pointerPos):
        if state == FPEventDispatcher.FPEventDispatcher.PRESSED:
            obj = FreeCAD.ActiveDocument.getObject(objName)
            pressEventLocationXY[objName] = pointerPos
            offsetDistanceAtPress[objName] = obj.OffsetDistance
            FPEventDispatcher.eventDispatcher.registerForLocation(objName, self.onDragged)
        else:
            FPEventDispatcher.eventDispatcher.unregisterForLocation(objName, self.onDragged)

        
    def onDragged(self, objName, pointerPos):
        # Used coordinate sytem names
        # K0 -> Part1 -> ... -> PartN(parentPart) -> ObjPlacement -> OnObjectPlacement

        obj = FreeCAD.ActiveDocument.getObject(objName)
        parentPartPlacement = FPUtils.getParentPartPlacement(obj) 
        # p0->p1 is the vector movement on screen(camera plane) 
        p0 = FreeCAD.Vector(pressEventLocationXY[objName][0], pressEventLocationXY[objName][1], 0)
        p1 = FreeCAD.Vector(pointerPos[0], pointerPos[1], 0)
        
        # transformed into Base coordinate system of the document
        camOrientation = FreeCADGui.activeDocument().activeView().getCameraOrientation()
        pointerDeltaInK0 = camOrientation.multVec(p1 - p0)
        # normalized fader direction vector in K0 coordinate system
        v0 = parentPartPlacement.Rotation.multVec(obj.PositiveDirection.normalize())

        cam = FreeCADGui.ActiveDocument.ActiveView.getCameraNode()
        camPosValues = cam.position.getValue()
        CamPos = FreeCAD.Vector(camPosValues[0], camPosValues[1], camPosValues[2])
        cam2ObjDist = (parentPartPlacement.multVec(obj.Group[0].Placement.Base) - CamPos).Length

        self.setDistance(obj, offsetDistanceAtPress[objName] + (v0.dot(pointerDeltaInK0) * cam2ObjDist / 1000))

    def getValue(self, objName):
        obj = FreeCAD.ActiveDocument.getObject(objName)
        aChild = obj.Group[0]
        fullDist = obj.NegativeDistLimit + obj.PositiveDistLimit
        ratio = (obj.NegativeDistLimit * obj.PositiveDirection  + (aChild.Placement.Base - self.getInitialPlacement(obj, aChild.Name).Base)).Length / float(fullDist)
        return int(ratio * float(obj.Resolution))

    def moveToValue(self, objName, value):
        obj = FreeCAD.ActiveDocument.getObject(objName)
        destDistance = ((value * float(obj.NegativeDistLimit + obj.PositiveDistLimit)) / float(obj.Resolution)) - obj.NegativeDistLimit
        self.setDistance(obj, destDistance)

    def setDistance(self, obj, destDistance):
        obj.OffsetDistance = FPUtils.clamp( destDistance, -obj.NegativeDistLimit, obj.PositiveDistLimit )            
        for child in obj.Group:
            child.Placement.Base = self.getInitialPlacement(obj, child.Name).Base + (obj.PositiveDirection.normalize() * obj.OffsetDistance)


class FPSimLinearPotentiometerViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        import FPSimDir
        return FPSimDir.__dir__ + '/icons/LinearPotentiometer.svg'

def createFPSimLinearPotentiometer():
    obj = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'FPSimLinearPotentiometer')
    FPSimLinearPotentiometer(obj)
    FPSimLinearPotentiometerViewProvider(obj.ViewObject)

    selection = FreeCAD.Gui.Selection.getSelectionEx()
    for sel_obj in selection:
        obj.addObject(sel_obj.Object)        
