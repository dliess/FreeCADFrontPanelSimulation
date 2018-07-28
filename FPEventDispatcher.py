import FreeCADGui
import FreeCAD
from pivy import coin
import time

class FPEventDispatcher:
    PRESSED = 0
    RELEASED = 1
    HOVER_IN = 0
    HOVER_OUT = 1

    def __init__(self):
        self._view              = None
        self._eventHandle       = None
        self._activeObj         = None
        self._activeObjKeypress = None
        self._prevHOverObj      = None

        self._buttonEventSubscribers   = dict()
        self._hOverSubscribers         = dict()
        self._locationSubscribers      = dict()
        self._keyEventSubscribers      = dict()
        self._hoverKeyEventSubscribers = dict()

        #self._lastPos = None

    def _handleEvent(self, eventObj):
        event = eventObj.getEvent()
        if event.getTypeId() == coin.SoKeyboardEvent.getClassTypeId():
            #FreeCAD.Console.PrintMessage("FPEventDispatcher: We are in SoKeyboardEvent " + str(event.getKey()) + "\n" )
            if event.getKey() in self._keyEventSubscribers:
                for objName in self._keyEventSubscribers[event.getKey()]:
                    state = FPEventDispatcher.PRESSED if event.getState() == event.DOWN else FPEventDispatcher.RELEASED
                    self._keyEventSubscribers[event.getKey()][objName](objName, event.getKey(), state)

            if event.getKey() in self._hoverKeyEventSubscribers:
                pos = event.getPosition().getValue()
                objDict = self._hoverKeyEventSubscribers[event.getKey()]
                if event.getState() == event.DOWN:
                    keyPressedObj = self._getObjAtPos(pos, objDict)
                    self._activeObjKeypress = keyPressedObj
                    if keyPressedObj:
                        objDict[keyPressedObj](keyPressedObj, event.getKey(), FPEventDispatcher.PRESSED)
                else:
                    if self._activeObjKeypress in objDict:
                        objDict[self._activeObjKeypress](self._activeObjKeypress, event.getKey(), FPEventDispatcher.RELEASED) 
                    self._activeObjKeypress = None

        elif event.getTypeId() == coin.SoLocation2Event.getClassTypeId():
            #FreeCAD.Console.PrintMessage("FPEventDispatcher: We are in SoLocation2Event\n")
            pos = event.getPosition().getValue()
            for objName in self._locationSubscribers:
                self._locationSubscribers[objName](objName, pos)
            ### This is some code to interpolate mouse pointer jumps, but it makes
            ### user experience baaaad
            #if not self._lastPos:
            #    self._lastPos = pos
            #delta = [ pos[0] - self._lastPos[0], pos[1] - self._lastPos[1]]
            #steps = max(abs(delta[0]), abs(delta[1]))
            #posToSend = [0,0]
            #for i in range(steps):
            #    step = i + 1
            #    posToSend[0] = self._lastPos[0] + int(float(delta[0] * step) / float(steps))
            #    posToSend[1] = self._lastPos[1] + int(float(delta[1] * step) / float(steps))
            #    for objName in self._locationSubscribers:
            #        self._locationSubscribers[objName](objName, posToSend)
            #    if step < steps:
            #        time.sleep(0.0001)
            #self._lastPos = pos
            
            newHOverObj = self._getObjAtPos(pos, self._hOverSubscribers)
            # HOver change
            if newHOverObj != self._prevHOverObj:
                if self._prevHOverObj in self._hOverSubscribers:
                    if (not self._activeObj) or (self._prevHOverObj == self._activeObj):
                        self._hOverSubscribers[self._prevHOverObj](self._prevHOverObj, FPEventDispatcher.HOVER_OUT)
                if newHOverObj in self._hOverSubscribers:
                    if (not self._activeObj) or (newHOverObj == self._activeObj):
                        self._hOverSubscribers[newHOverObj](newHOverObj, FPEventDispatcher.HOVER_IN)
                self._prevHOverObj = newHOverObj
                
        elif event.getTypeId() == coin.SoMouseButtonEvent.getClassTypeId():
            #FreeCAD.Console.PrintMessage("FPEventDispatcher: We are in SoMouseButtonEvent")
            pos = event.getPosition().getValue()
            if event.getState() == event.DOWN:
                clickedObj = self._getObjAtPos(pos, self._buttonEventSubscribers)
                self._activeObj = clickedObj
                if clickedObj in self._buttonEventSubscribers:
                    self._buttonEventSubscribers[clickedObj](clickedObj, FPEventDispatcher.PRESSED, pos)
            else:
                if self._activeObj in self._buttonEventSubscribers:
                    self._buttonEventSubscribers[self._activeObj](self._activeObj, FPEventDispatcher.RELEASED, pos) 
                self._activeObj = None
        else:
            FreeCAD.Console.PrintMessage("FPEventDispatcher: We are in nothing" + event.getTypeId().getName() + "\n")

    def _getObjAtPos(self, pos, objList):
        listObjects = self._view.getObjectsInfo((int(pos[0]),int(pos[1])))
        if listObjects:
            # only inspect upmost object in respect to the camera
            objName = listObjects[0]["Object"]
            #FreeCAD.Console.PrintMessage("FPEventDispatcher: upmost object is: " + objName + "\n") 
            if objName in objList:
                return objName
            else:
                # when not found search parent tree up until first match
                for parentObject in FreeCAD.ActiveDocument.getObject(objName).InListRecursive:
                    if parentObject.Name in objList:
                        return parentObject.Name
        return None

    def _disableObjectSelection(self):
        self._view.getSceneGraph().getField("selectionRole").setValue(0)
        return

    def _enableObjectSelection(self):
        self._view.getSceneGraph().getField("selectionRole").setValue(1)
        return

    # ******** public interface *********

    def activate(self):
        self._view =  FreeCADGui.ActiveDocument.ActiveView
        self._disableObjectSelection()
        self._eventHandle = self._view.addEventCallbackPivy( coin.SoEvent.getClassTypeId(), self._handleEvent )
        return  

    def deactivate(self):
        self._view.removeEventCallbackPivy( coin.SoEvent.getClassTypeId(), self._eventHandle )
        self._enableObjectSelection()
        self._view = None
        return

    def registerForButtonEvent(self, objName, cb):
        # pass objName, PRESS/RELEASE and location
        self._buttonEventSubscribers[objName] = cb 

    def unregisterForButtonEvent(self, objName):
        if objName in self._buttonEventSubscribers:
            del self._buttonEventSubscribers[objName]

    def registerForLocation(self, objName, cb):
        # pass objName, position 
        self._locationSubscribers[objName] = cb 
        
    def unregisterForLocation(self, objName, cb):
        if objName in self._locationSubscribers:
            del self._locationSubscribers[objName]

    def registerForHOver(self, objName, cb):
        # pass objName, HOVER_IN/HOVER_OUT
        # Only call when there is no active oject or object is the active object
        self._hOverSubscribers[objName] = cb 

    def unregisterForHOver(self, objName):
        if objName in self._hOverSubscribers:
            del self._hOverSubscribers[objName]

    def registerForKeyPress(self, objName, key, cb):
        if key not in self._keyEventSubscribers:
            self._keyEventSubscribers[key] = dict()
        self._keyEventSubscribers[key][objName] = cb

    def unregisterKeyPress(self, objName, key):
        if key in self._keyEventSubscribers:
            if objName in self._keyEventSubscribers[key]:
                del self._keyEventSubscribers[key][objName]

    def registerForHoverKeyPress(self, objName, key, cb):
        if key not in self._hoverKeyEventSubscribers:
            self._hoverKeyEventSubscribers[key] = dict()
        self._hoverKeyEventSubscribers[key][objName] = cb

    def unregisterHoverKeyPress(self, objName, key):
        if key in self._hoverKeyEventSubscribers:
            if objName in self._hoverKeyEventSubscribers[key]:
                del self._hoverKeyEventSubscribers[key][objName]
    
eventDispatcher = FPEventDispatcher()
        
