import FreeCAD
import FPEventDispatcher
from FPInitialPlacement import InitialPlacements
import FPSimServer
import FPUtils

pressEventLocationXY = dict()
rotationAngleAtPress = dict()

class FPSimRotaryPotentiometer(InitialPlacements):
    def __init__(self, obj):
        InitialPlacements.__init__(self, obj)
        obj.addProperty('App::PropertyPythonObject', 'RotationAngleDeg').RotationAngleDeg = 0
        obj.addProperty('App::PropertyInteger', 'IncrementsOnWholeArc').IncrementsOnWholeArc = 64
        obj.addProperty('App::PropertyFloat', 'MouseSensitivity').MouseSensitivity = 1.0
        obj.addProperty('App::PropertyVector', 'RotationAxis').RotationAxis = (0,0,0)
        obj.addProperty('App::PropertyVector', 'RotationCenter').RotationCenter = (0,0,0)
        obj.addProperty('App::PropertyFloat', 'PositiveRotLimitDeg').PositiveRotLimitDeg = 10.0
        obj.addProperty('App::PropertyFloat', 'NegativeRotLimitDeg').NegativeRotLimitDeg = 10.0
        obj.addProperty('App::PropertyInteger', 'NumSnapInPositions').NumSnapInPositions = 0
        obj.addProperty('App::PropertyBool', 'Motorized').Motorized = False
        obj.addProperty('App::PropertyBool', 'TouchSensitive').TouchSensitive = False

        obj.Proxy = self

    def _registerEventCallbacks(self, objName):
        FPEventDispatcher.eventDispatcher.registerForButtonEvent(objName, self.onButtonEvent)

    def _unregisterEventCallbacks(self, objName):
        FPEventDispatcher.eventDispatcher.unregisterForButtonEvent(objName)

    def onChanged(self, obj, prop):
        #FreeCAD.Console.PrintMessage("in onChanged obj.Name: " + str(obj.Name) + " obj.Label: " + str(obj.Label) + " prop: " + str(prop) + "\n")
        if prop == 'Proxy':
            # Called at loading existing object on first place(Placement is not valid yet )
            # Called at creation on first place(ToCheck: I think Placement is not valid here yet)
            self._registerEventCallbacks(obj.Name)
            FPSimServer.dataAquisitionCBHolder.setPotentiometerCB(obj.Name, self.getValue)
        elif prop == 'Group':
            # Always called when the group changes(new group member inserted or removed) 
            # or gets created :
            #    - called after 'proxy'-cb
            #    - Placement is valid
            #    - strange thing is at this point there is no child object inside
            if not obj.Group:
                # Called when Removing all objects from group or when group-obj gets deleted
                #FreeCAD.Console.PrintMessage(str(obj.Label) + " Obj has no Group attribute\n")
                FPSimServer.dataAquisitionCBHolder.clearPotentiometerCB(obj.Name)
                self._unregisterEventCallbacks(obj.Name)
            elif self.hasNoChilds(obj):
                # Called at object creation
                #FreeCAD.Console.PrintMessage(str(obj.Label) + " Obj has Group attribute but no childs\n")
                FPSimServer.dataAquisitionCBHolder.setPotentiometerCB(obj.Name, self.getValue)
                self._registerEventCallbacks(obj.Name)
            else:
                # Called When object gets added to a group that already has at least one child
                #FreeCAD.Console.PrintMessage(str(obj.Label) + " Obj has Group attribute and childs\n")
                pass
            self.saveInitialPlacements(obj) 
        elif prop == 'ExpressionEngine':
            # Called at loading existing object at last cb(Placement is valid now)
            try:
                obj.RotationAngleDeg = 0
                self.moveToInitialPlacement(obj)
            except KeyError:
                self.saveInitialPlacements(obj)

        elif prop == 'NumSnapInPositions':
            if obj.NumSnapInPositions == 1:
                obj.NumSnapInPositions = 2
            if obj.NumSnapInPositions < 0:
                obj.NumSnapInPositions = 0
            # Called on parameter change (followed by execute-cb when it gets applied)

    def execute(self, fp):
        #FreeCAD.Console.PrintMessage("in execute fp: " + str(fp.Label) + "\n")
        # Called when group-obj parameter change or child-objects parameter change gets applied
        pass

    def onButtonEvent(self, objName, state, pointerPos):
        if state == FPEventDispatcher.FPEventDispatcher.PRESSED:
            obj = FreeCAD.ActiveDocument.getObject(objName)
            pressEventLocationXY[objName] = pointerPos
            rotationAngleAtPress[objName] = obj.RotationAngleDeg
            FPEventDispatcher.eventDispatcher.registerForLocation(objName, self.onDragged)
        else:
            FPEventDispatcher.eventDispatcher.unregisterForLocation(objName, self.onDragged)

    def onDragged(self, objName, pointerPos):
        obj = FreeCAD.ActiveDocument.getObject(objName)
        self.setRotation(obj, rotationAngleAtPress[objName] + (pointerPos[1] - pressEventLocationXY[objName][1]) * obj.MouseSensitivity)

    def getValue(self, objName):
        obj = FreeCAD.ActiveDocument.getObject(objName)
        wholeArcDeg = obj.NegativeRotLimitDeg + obj.PositiveRotLimitDeg
        rotDeg = obj.RotationAngleDeg + obj.NegativeRotLimitDeg
        return int( (rotDeg / wholeArcDeg) * float(obj.IncrementsOnWholeArc - 1) )

    def moveToValue(self, objName, value):
        obj = FreeCAD.ActiveDocument.getObject(objName)
        fullRangeDeg = obj.NegativeRotLimitDeg + obj.PositiveRotLimitDeg
        destDeg = value * float(fullRangeDeg) / float(obj.IncrementsOnWholeArc) - obj.NegativeRotLimitDeg
        self.setRotation(obj, destDeg)

    def setRotation(self, obj, degree):
        clampedDeg = FPUtils.clamp(degree, -obj.PositiveRotLimitDeg, obj.NegativeRotLimitDeg)
        if obj.NumSnapInPositions:
            partDeg = float(obj.NegativeRotLimitDeg + obj.PositiveRotLimitDeg) / float(obj.NumSnapInPositions - 1)
            obj.RotationAngleDeg = int((obj.NegativeRotLimitDeg + clampedDeg) / partDeg) * partDeg - obj.NegativeRotLimitDeg
        else:
            obj.RotationAngleDeg = clampedDeg
        rot = FreeCAD.Rotation(obj.RotationAxis, obj.RotationAngleDeg)
        for child in obj.Group:
            initPlc = self.getInitialPlacement(obj, child.Name)
            rotPlacement = FreeCAD.Placement(initPlc.Base, rot, obj.RotationCenter - initPlc.Base)
            newRot = rotPlacement.Rotation.multiply( initPlc.Rotation )
            newBase = rotPlacement.Base
            child.Placement.Base = newBase
            child.Placement.Rotation = newRot
        


class FPSimRotaryPotentiometerViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        import FPSimDir
        return FPSimDir.__dir__ + '/icons/RotPotentiometer.svg'

def createFPSimRotaryPotentiometer():
    obj = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'FPSimRotaryPotentiometer')
    FPSimRotaryPotentiometer(obj)
    FPSimRotaryPotentiometerViewProvider(obj.ViewObject)

    selection = FreeCAD.Gui.Selection.getSelectionEx()
    try:
        obj.RotationAxis = selection[-1].SubObjects[-1].normalAt(0,0)
        obj.RotationCenter = selection[-1].SubObjects[-1].CenterOfMass
        for sel_obj in selection:
            obj.addObject(sel_obj.Object)
    except IndexError:
        FreeCAD.Console.PrintError("Usage Error, select objects and a rotation surface\n")
        
