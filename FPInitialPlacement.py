import FreeCAD

class InitialPlacements:
    def __init__(self, obj):
        obj.addProperty('App::PropertyPythonObject', 'InitialPlacements').InitialPlacements = {}

    def saveInitialPlacements(self, obj):
        obj.InitialPlacements.clear()
        for child in obj.Group:
            plm = child.Placement
            base = (plm.Base[0], plm.Base[1], plm.Base[2])
            rot = plm.Rotation.Q
            placement = (base, rot)
            obj.InitialPlacements[child.Name] = placement

    def getInitialPlacement(self, obj, childName):
        plm = obj.InitialPlacements[childName]
        placement = FreeCAD.Placement()
        placement.Base = FreeCAD.Vector(plm[0][0], plm[0][1], plm[0][2])
        placement.Rotation = FreeCAD.Rotation(plm[1][0], plm[1][1], plm[1][2], plm[1][3])
        return placement

    def hasNoChilds(self, obj):
        return len( obj.InitialPlacements ) == 0

    def moveToInitialPlacement(self, obj):
        for child in obj.Group:
            child.Placement = self.getInitialPlacement(obj, child.Name)
        

