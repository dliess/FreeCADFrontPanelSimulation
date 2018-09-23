import FreeCAD
import FreeCADGui
import FPEventDispatcher
import FPSimServer
import FPUtils

pressedPosition = dict()

class FPSimTouchSurface:
    def __init__(self, obj):
        obj.addProperty('App::PropertyPythonObject', 'SurfacePlacement').SurfacePlacement = None
        obj.addProperty('App::PropertyPythonObject', 'XLen').XLen = 0.0
        obj.addProperty('App::PropertyPythonObject', 'YLen').YLen = 0.0
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
            else:
                self._registerEventCallbacks(obj.Name)
            #FreeCAD.Console.PrintMessage("Group cb: Saving initial Placement\n")
        elif prop == 'ExpressionEngine':
            #FreeCAD.Console.PrintMessage("ExpressionEngine\n")
            # Called at loading existing object at last cb(Placement is valid now)
            pass
        elif prop == 'ResolutionX':
            if 'ResolutionY' in obj.PropertiesList:
                pass
        elif prop == 'ResolutionY':
            if 'ResolutionX' in obj.PropertiesList:
                pass

    def execute(self, fp):
        # moving objects in group result in calling this, so reset initial placements to new pos
        pass

    def onButtonEvent(self, objName, state, pos):
        if state == FPEventDispatcher.FPEventDispatcher.PRESSED:
            FPEventDispatcher.eventDispatcher.registerForLocation(objName, self.onLocationEvent)
            self.pointerPosToTouchSurfaceCoord(objName, pos)
        else:
            FPEventDispatcher.eventDispatcher.unregisterForLocation(objName, self.onLocationEvent)
            pressedPosition[objName] = (-1 , -1)

    def onLocationEvent(self, objName, pos):
        self.pointerPosToTouchSurfaceCoord(objName, pos)

    def pointerPosToTouchSurfaceCoord(self, objName, pos):
        objInfo = FreeCADGui.ActiveDocument.ActiveView.getObjectInfo((pos[0], pos[1]))
        if objInfo:
            vec = FreeCAD.Vector(objInfo['x'], objInfo['y'], objInfo['z'])
            obj = FreeCAD.ActiveDocument.getObject(objName)
            if obj.Group[0]:
                #FreeCAD.Console.PrintMessage(str(vec) + " xlen: " + str(obj.XLen) + " ylen: " + str(obj.YLen) +"\n")
                childPlacement = obj.Group[0].Placement
                frameToK0 = FPUtils.getParentPartPlacement(obj).multiply(childPlacement.multiply(FPUtils.propertyPythonObjectToFreeCADPlacement(obj.SurfacePlacement))).inverse()
                vecInSurface = frameToK0.multVec(vec)
                if vecInSurface.x >= 0.0 and vecInSurface.x < obj.XLen and vecInSurface.y >= 0.0 and vecInSurface.y < obj.YLen:
                    x = int( (vecInSurface.x * float(obj.ResolutionX)) / obj.XLen )
                    y = int( (vecInSurface.y * float(obj.ResolutionY)) / obj.YLen )
                    pressedPosition[objName] = (x , y)
                    #FreeCAD.Console.PrintMessage("obj: " + str(objInfo['Object']) + " touch vector: " + str(vecInSurface) + " | " +str(pressedPosition[objName]) + "\n")
                    FPSimServer.dataAquisitionCBHolder.setTouchSurfaceCB(objName, self.getPointedPosition)

    def getPointedPosition(self, objName):
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

    selection = FreeCAD.Gui.Selection.getSelectionEx()
    if selection:
        selObject = selection[0].Object
        subObject = selection[0].SubObjects
        edgeX = subObject[0]
        edgeY = subObject[1]
        if edgeX.ShapeType != 'Edge' or edgeY.ShapeType != 'Edge':
            FreeCAD.Console.PrintError("Error in creating Touch Surface, usage: First selected item must be the edge representing the x-axis then the y-axis\n")
            return
        origin = None
        iVector = None
        jVector = None
        for i in range(2):
            for j in range(2):
                if edgeX.Vertexes[i].Point == edgeY.Vertexes[j].Point:
                    if i == 0:
                        iVector = FreeCAD.Vector(edgeX.Vertexes[1].Point - edgeX.Vertexes[0].Point)
                    else:
                        iVector = FreeCAD.Vector(edgeX.Vertexes[0].Point - edgeX.Vertexes[1].Point)
                    if j == 0:
                        jVector = FreeCAD.Vector(edgeY.Vertexes[1].Point - edgeY.Vertexes[0].Point)
                    else:
                        jVector = FreeCAD.Vector(edgeY.Vertexes[0].Point - edgeY.Vertexes[1].Point)                                                
                    origin = edgeX.Vertexes[i].Point
                    break
            if origin:
                break
        if not origin:
            FreeCAD.Console.PrintError("Error in creating Touch Surface, selected edges must have a common origin\n")
            return
        xLen = iVector.Length
        iVector = iVector.normalize()
        yLen = jVector.Length
        jVector = jVector.normalize()

        kVector = iVector.cross(jVector)

        if not FPUtils.isClose(kVector.Length, 1.0):
            FreeCAD.Console.PrintError("Error in creating Touch Surface, selected edges must be perpendicualar (kVector.Length is " + str(kVector.Length) + "))\n")
            return
        matrix = FreeCAD.Matrix( iVector[0], jVector[0], kVector[0], origin[0],
                                 iVector[1], jVector[1], kVector[1], origin[1],
                                 iVector[2], jVector[2], kVector[2], origin[2],
                                 0,          0,          0,         1 )
        surfacePlacement = selObject.Placement.inverse().multiply(FreeCAD.Placement(matrix))
        obj.SurfacePlacement = FPUtils.freeCADPlacementToPropertyPythonObject(surfacePlacement)
        obj.XLen = xLen
        obj.YLen = yLen
        obj.addObject(selObject)
        
