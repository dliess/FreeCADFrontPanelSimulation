import FreeCAD
import FPUtils

class InitialPlacements:
    def __init__(self, obj):
        obj.addProperty('App::PropertyPythonObject', 'InitialPlacements').InitialPlacements = {}

    def saveInitialPlacements(self, obj):
        obj.InitialPlacements.clear()
        for child in obj.Group:
            placement = FPUtils.freeCADPlacementToPropertyPythonObject(child.Placement)
            obj.InitialPlacements[child.Name] = placement

    def getInitialPlacement(self, obj, childName):
        return FPUtils.propertyPythonObjectToFreeCADPlacement(obj.InitialPlacements[childName])

    def hasNoChilds(self, obj):
        return len( obj.InitialPlacements ) == 0

    def moveToInitialPlacement(self, obj):
        for child in obj.Group:
            child.Placement = self.getInitialPlacement(obj, child.Name)
        

