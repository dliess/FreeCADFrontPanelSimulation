import FreeCAD
import FPEventDispatcher
import FPSimServer

pressedPosition = dict()

class FPSimTouchSurface:
    def __init__(self, obj):
        obj.addProperty('App::PropertyInteger', 'ResolutionX').ResolutionX = 10
        obj.addProperty('App::PropertyInteger', 'ResolutionY').ResolutionY = 10
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
        elif prop == 'ExpressionEngine':
            #FreeCAD.Console.PrintMessage("ExpressionEngine\n")
            # Called at loading existing object at last cb(Placement is valid now)
            pass

    def execute(self, fp):
        # moving objects in group result in calling this, so reset initial placements to new pos
        pass

    def onButtonEvent(self, objName, state, pos):
        if state == FPEventDispatcher.FPEventDispatcher.PRESSED:
            FPSimServer.dataAquisitionCBHolder.setTouchSurfaceCB(objName, self.getPointedPosition)
            objInfo = FreeCADGui.ActiveDocument.ActiveView.getObjectInfo(pos)
            pressedPosition[objName] = objInfo
            #TODO
            #'Document': 'Unnamed', 'Object': 'Box', 'Component': 'Face5', 'y': 0.05458798632025719, 'x': 9.842083930969238, 'z': 0.0

    def getPointedPosition(self, objName):
        FPSimServer.dataAquisitionCBHolder.clearTouchSurfaceCB(objName)
        return pressedPosition[objName]

class FPSimTouchSurfaceViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        import FPSimDir
        return FPSimDir.__dir__ + '/icons/TouchSurface.svg'


def createFPSimTouchSurface():
    obj = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'FPSimTouchSurface')
    FPSimTouchSurface(obj)
    FPSimTouchSurfaceViewProvider(obj.ViewObject)

    selection = FreeCAD.Gui.Selection.getSelection()
    for selObj in selection:
        obj.addObject(selObj)
        
