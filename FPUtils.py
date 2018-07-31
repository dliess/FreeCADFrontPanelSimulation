import FreeCAD

def getFramePlacement(obj):
    placementList = []
    objToInspect = obj
    while True:
        parentPart = None
        for parent in objToInspect.InList:
            if parent.TypeId == 'App::Part':
                placementList.append(parent.Placement)
                parentPart = parent
        if parentPart:
           objToInspect = parentPart
        else:
            break
    ret = FreeCAD.Placement()
    placementList.reverse()
    for p in placementList:
        ret = ret.multiply(p)
    return ret

def freeCADPlacementToPropertyPythonObject(freeCADPlacement):
    plm = freeCADPlacement
    base = (plm.Base[0], plm.Base[1], plm.Base[2])
    rot = plm.Rotation.Q
    placement = (base, rot)
    return placement

def propertyPythonObjectToFreeCADPlacement(plm):
    placement = FreeCAD.Placement()
    placement.Base = FreeCAD.Vector(plm[0][0], plm[0][1], plm[0][2])
    placement.Rotation = FreeCAD.Rotation(plm[1][0], plm[1][1], plm[1][2], plm[1][3])
    return placement

def isClose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
