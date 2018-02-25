import FreeCAD
import FPEventDispatcher
from FPInitialPlacement import InitialPlacements
import FPSimServer
import generated.FPSimulation_pb2 as Proto

buttonState = dict()

class FPSimButton(InitialPlacements):
    def __init__(self, obj):
        InitialPlacements.__init__(self, obj)
        buttonState[obj.Name] = Proto.BUTTON_RELEASED
        obj.addProperty('App::PropertyVector', 'RotationAxis').RotationAxis = (0,0,0)
        obj.addProperty('App::PropertyFloat', 'RotationAngle').RotationAngle = 0
        obj.addProperty('App::PropertyVector', 'RotationCenter').RotationCenter = (0,0,0)
        obj.addProperty('App::PropertyVector', 'Translation').Translation = (0,0,0)
        obj.Proxy = self

    def _registerEventCallbacks(self, objName):
        FPEventDispatcher.eventDispatcher.registerForButtonEvent(objName, self.onButtonEvent)

    def _unregisterEventCallbacks(self, objName):
        FPEventDispatcher.eventDispatcher.unregisterForButtonEvent(objName)

    def onChanged(self, obj, prop):
        if prop == 'Proxy':
            self._registerEventCallbacks(obj.Name)
        elif prop == 'Group':
            if not obj.Group:
                self._unregisterEventCallbacks(obj.Name)
            elif self.hasNoChilds(obj):
                self._registerEventCallbacks(obj.Name)
            self.saveInitialPlacements(obj) # needed at creation

    def execute(self, fp):
        # moving objects in group result in calling this, so reset initial placements to new pos
        pass

    def onButtonEvent(self, objName, state, pos):
        obj = FreeCAD.ActiveDocument.getObject(objName)

        FPSimServer.dataAquisitionCBHolder.setButtonCB(objName, self.getState)
        rot = FreeCAD.Rotation(obj.RotationAxis, obj.RotationAngle)
        for child in obj.Group:
            if state == FPEventDispatcher.FPEventDispatcher.PRESSED:
                pos = child.Placement.Base + obj.Translation
                rotPlacement = FreeCAD.Placement(pos, rot, obj.RotationCenter - child.Placement.Base)
                newRot = rotPlacement.Rotation.multiply( child.Placement.Rotation )
                newBase = rotPlacement.Base
                child.Placement.Base = newBase
                child.Placement.Rotation = newRot
                buttonState[objName] = Proto.BUTTON_PRESSED
            else:
                child.Placement = self.getInitialPlacement(obj, child.Name)
                buttonState[objName] = Proto.BUTTON_RELEASED

        
    def getState(self, objName):
        FPSimServer.dataAquisitionCBHolder.clearButtonCB(objName)
        obj = FreeCAD.ActiveDocument.getObject(objName)
        return buttonState[objName]


class FPSimButtonViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        import FPSimDir
        return FPSimDir.__dir__ + '/icons/Button.svg'

def createFPSimRotButton():
    buttonObj = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'FPSimButton')
    FPSimButton(buttonObj)
    FPSimButtonViewProvider(buttonObj.ViewObject)

    selection = FreeCAD.Gui.Selection.getSelectionEx()
    try:
        buttonObj.RotationAxis = selection[-1].SubObjects[-1].normalAt(0,0)
        buttonObj.RotationCenter = selection[-1].SubObjects[-1].CenterOfMass
        for sel_obj in selection:
            buttonObj.addObject(sel_obj.Object)
    except IndexError:
        FreeCAD.Console.PrintError("Usage Error, select objects and a rotation surface\n")
        

def createFPSimLinButton():
    buttonObj = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'FPSimButton')
    FPSimButton(buttonObj)
    FPSimButtonViewProvider(buttonObj.ViewObject)

    selection = FreeCAD.Gui.Selection.getSelectionEx()
    try:
        buttonObj.Translation = selection[-1].SubObjects[-1].normalAt(0, 0).negative()
        for sel_obj in selection:
            buttonObj.addObject(sel_obj.Object)
    except IndexError:
        FreeCAD.Console.PrintError("Usage Error, select objects and a surface\n")

