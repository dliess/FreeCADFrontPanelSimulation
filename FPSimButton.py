import FreeCAD
import FPEventDispatcher
import FPUtils
from FPInitialPlacement import InitialPlacements
import FPSimServer
import generated.python.FPSimulation_pb2 as Proto

buttonState = dict()

def has5dButtonTraits(buttonObj):
    return hasattr(buttonObj, 'PressureResolutionLin') and \
           (buttonObj.PressureResolutionLin.x != 0 or buttonObj.PressureResolutionLin.y != 0)

def has3dButtonTraits(buttonObj):
    return (hasattr(buttonObj, 'PressureResolutionLin') and (buttonObj.PressureResolutionLin.z != 0)) or \
           (hasattr(buttonObj, 'VelocityResolution')    and (buttonObj.VelocityResolution != 0))

class FPSimButton(InitialPlacements):
    def __init__(self, obj):
        InitialPlacements.__init__(self, obj)
        buttonState[obj.Name] = Proto.BUTTON_RELEASED
        obj.addProperty('App::PropertyVector', 'RotationAxis').RotationAxis = (0,0,0)
        obj.addProperty('App::PropertyFloat', 'RotationAngle').RotationAngle = 0
        obj.addProperty('App::PropertyVector', 'RotationCenter').RotationCenter = (0,0,0)
        obj.addProperty('App::PropertyVector', 'Translation').Translation = (0,0,0)
        obj.addProperty('App::PropertyBool', 'SwitchMode').SwitchMode = False
        obj.addProperty('App::PropertyVector', 'PressureResolutionLin').PressureResolutionLin = (0,0,0)
        obj.addProperty('App::PropertyVector', 'PressureResolutionAng').PressureResolutionAng = (0,0,0)
        obj.addProperty('App::PropertyInteger', 'VelocityResolution').VelocityResolution = 0
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
        elif prop == 'Group':
            # Always called when the group changes(new group member inserted or removed) 
            # or gets created :
            #    - called after 'proxy'-cb
            #    - Placement is valid
            #    - strange thing is at this point there is no child object inside
            if not obj.Group:
                # Called when Removing all objects from group or when group-obj gets deleted
                #FreeCAD.Console.PrintMessage(str(obj.Label) + " Obj has no Group attribute\n")    
                self._unregisterEventCallbacks(obj.Name)
            elif self.hasNoChilds(obj):
                # Called at object creation
                #FreeCAD.Console.PrintMessage(str(obj.Label) + " Obj has Group attribute but no childs\n")
                self._registerEventCallbacks(obj.Name)
            #FreeCAD.Console.PrintMessage("Group cb: Saving initial Placement\n")
            self.saveInitialPlacements(obj) # needed at creation
        elif prop == 'ExpressionEngine':
            #FreeCAD.Console.PrintMessage("ExpressionEngine\n")
            # Called at loading existing object at last cb(Placement is valid now)
            try:
                #FreeCAD.Console.PrintMessage("Move to initial placement\n")
                self.moveToInitialPlacement(obj)
            except KeyError:
                #FreeCAD.Console.PrintMessage("Key Error exception\n")
                self.saveInitialPlacements(obj)


    def execute(self, fp):
        # moving objects in group result in calling this, so reset initial placements to new pos
        pass

    def onButtonEvent(self, objName, state, pos):
        obj = FreeCAD.ActiveDocument.getObject(objName)
        FreeCAD.Console.PrintMessage("onButtonEvent: " + objName + "\n")
        if(has5dButtonTraits(obj)):
            FPSimServer.dataAquisitionCBHolder.setButton5dCB(objName, self.getState)
        elif(has3dButtonTraits(obj)):
            FPSimServer.dataAquisitionCBHolder.setButton3dCB(objName, self.getState)
        else:
            FPSimServer.dataAquisitionCBHolder.setButtonCB(objName, self.getState)
        rot = FreeCAD.Rotation(obj.RotationAxis, obj.RotationAngle)
        if state == FPEventDispatcher.FPEventDispatcher.PRESSED:
            if not obj.SwitchMode:
                buttonState[objName] = Proto.BUTTON_PRESSED
            else:
                if buttonState[objName] == Proto.BUTTON_PRESSED:
                    buttonState[objName] = Proto.BUTTON_RELEASED
                elif buttonState[objName] == Proto.BUTTON_RELEASED:
                    buttonState[objName] = Proto.BUTTON_PRESSED
        else:
            if not obj.SwitchMode:
                buttonState[objName] = Proto.BUTTON_RELEASED
            else:
                return
        for child in FPUtils.getChildsWithPlacement(obj):
            if buttonState[objName] == Proto.BUTTON_PRESSED:
                pos = child.Placement.Base + obj.Translation
                rotPlacement = FreeCAD.Placement(pos, rot, obj.RotationCenter - child.Placement.Base)
                newRot = rotPlacement.Rotation.multiply( child.Placement.Rotation )
                newBase = rotPlacement.Base
                child.Placement.Base = newBase
                child.Placement.Rotation = newRot
            elif buttonState[objName] == Proto.BUTTON_RELEASED:
                child.Placement = self.getInitialPlacement(obj, child.Name)

        
    def getState(self, objName):
        FreeCAD.Console.PrintMessage("getState " + objName + "\n")
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
            theObj = sel_obj.Object
            if theObj.InList:
                for parent in theObj.InList:
                    buttonObj.addObject(parent)
            else:
                buttonObj.addObject(theObj)
    except IndexError:
        FreeCAD.Console.PrintError("Usage Error, select objects and a surface\n")
