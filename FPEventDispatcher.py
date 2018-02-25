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
        self._view         = None
        self._eventHandle  = None
        self._activeObj    = None
        self._prevHOverObj = None

        self._buttonEventSubscribers = dict()
        self._hOverSubscribers       = dict()
        self._locationSubscribers    = dict()
        self._keyEvent               = dict()

        #self._lastPos = None


    def _handleEvent(self, eventObj):
        event = eventObj.getEvent()
        if event.getTypeId() == coin.SoKeyboardEvent.getClassTypeId():
            #FreeCAD.Console.PrintMessage("FPEventDispatcher: We are in SoKeyboardEvent " + str(event.getKey()) + "\n" )
            if event.getKey() in self._keyEvent:
                tup = self._keyEvent[event.getKey()]
                if event.getState() == event.DOWN:
                    tup[1](tup[0], FPEventDispatcher.PRESSED)
                else:
                    tup[1](tup[0], FPEventDispatcher.RELEASED)

        elif event.getTypeId() == coin.SoLocation2Event.getClassTypeId():
            #FreeCAD.Console.PrintMessage("FPEventDispatcher: We are in SoLocation2Event\n")
            pos = event.getPosition().getValue()
            for objName in self._locationSubscribers:
                self._locationSubscribers[objName](objName, pos)
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
        # pass objName, up/down
        self._keyEvent[key] = (objName, cb)

    def unregisterKeyPress(self, key):
        if key in self._keyEvent:
            del self._keyEvent[key]

    
eventDispatcher = FPEventDispatcher()
        
