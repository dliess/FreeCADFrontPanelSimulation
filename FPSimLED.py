import FreeCAD

def setLEDColor(obj, colorRGB):
            obj = FreeCAD.ActiveDocument.getObjectsByLabel(obj.Name)[0]
            obj.ViewObject.ShapeColor = (colorRGB.red,
                                         colorRGB.green,
                                         colorRGB.blue,
                                         0.0)
            
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

