import FreeCAD

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
        obj.Proxy = self

    def setColor(self, obj, colorRGB):
        for child in obj.Group:
            child.ViewObject.ShapeColor = (colorRGB.red,
                                           colorRGB.green,
                                           colorRGB.blue, 
                                           0.0)
            child.touch()

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
