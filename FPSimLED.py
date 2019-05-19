import FreeCAD
import generated.python.FPSimulation_pb2 as Proto

            #from pivy import coin
            #FreeCAD.ActiveDocument.recompute()
            # rn = obj.ViewObject.RootNode

            # sa = coin.SoSearchAction()
            # sa.setType( coin.SoSwitch.getClassTypeId() )
            # sa.setSearchingAll(True)
            # sa.apply(rn)
            # switch = sa.getPath().getTail()
            # for childNode in switch.getChildren():
            #     sa1 = coin.SoSearchAction()
            #     sa1.setType( coin.SoMaterial.getClassTypeId() )
            #     sa1.setSearchingAll(True)
            #     sa1.apply(childNode)
            #     if sa1.isFound():
            #         FreeCAD.Console.PrintMessage("MaterialFound\n")
            #         mat = sa1.getPath().getTail()
            #         mat.diffuseColor = (request.color.red,
            #                             request.color.green,
            #                             request.color.blue)
            # FreeCAD.Console.PrintMessage("---------------------------\n")

                # else:
                #     FreeCAD.Console.PrintError("No material found for: " + obj.Name + "\n")
class FPSimLED:
    def __init__(self, obj):
        obj.addProperty('App::PropertyInteger', 'Unenlightened_Red').Unenlightened_Red = 0
        obj.addProperty('App::PropertyInteger', 'Unenlightened_Green').Unenlightened_Green = 0
        obj.addProperty('App::PropertyInteger', 'Unenlightened_Blue').Unenlightened_Blue = 0
        obj.Proxy = self

    def setColor(self, obj, color):
        unenlighted_red = 0 if not hasattr(obj, "Unenlightened_Red") else obj.Unenlightened_Red
        unenlighted_green = 0 if not hasattr(obj, "Unenlightened_Green") else obj.Unenlightened_Green
        unenlighted_blue = 0 if not hasattr(obj, "Unenlightened_Blue") else obj.Unenlightened_Blue

        r = unenlighted_red + (((255.0 - unenlighted_red) * color.r) / 255.0)
        g = unenlighted_green + (((255.0 - unenlighted_green) * color.g) / 255.0)
        b = unenlighted_blue + (((255.0 - unenlighted_blue) * color.b) / 255.0)
        for child in obj.Group:
            child.ViewObject.ShapeColor = (float(r) / 255.0,
                                           float(g) / 255.0,
                                           float(b) / 255.0, 
                                           float(color.a) / 255.0)
            child.touch()

    def onChanged(self, obj, prop):
        #FreeCAD.Console.PrintMessage("in onChanged obj.Name: " + str(obj.Name) + " obj.Label: " + str(obj.Label) + " prop: " + str(prop) + "\n")
        if prop == 'Proxy':
            # Called at loading existing object on first place(Placement is not valid yet )
            # Called at creation on first place(ToCheck: I think Placement is not valid here yet)
            pass
        elif prop == 'Group':
            # Always called when the group changes(new group member inserted or removed) 
            # or gets created :
            #    - called after 'proxy'-cb
            #    - Placement is valid
            #    - strange thing is at this point there is no child object inside
            if not obj.Group:
                # Called when Removing all objects from group or when group-obj gets deleted
                #FreeCAD.Console.PrintMessage(str(obj.Label) + " Obj has no Group attribute\n")
                pass
        elif prop == 'ExpressionEngine' or\
             prop == 'Unenlightened_Red' or prop == 'Unenlightened_Green' or prop == 'Unenlightened_Blue':
            # Called at loading existing object at last cb(Placement is valid now)
            color = Proto.Color(r = 0, g = 0, b = 0, a = 255)
            self.setColor(obj, color)

class FPSimLEDViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

    def getIcon(self):
        import FPSimDir
        return FPSimDir.__dir__ + '/icons/LED.svg'


def createFPSimLED():
    obj = FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython', 'FPSimLED')
    FPSimLED(obj)
    FPSimLEDViewProvider(obj.ViewObject)

    selection = FreeCAD.Gui.Selection.getSelection()
    for selObj in selection:
        obj.addObject(selObj)
