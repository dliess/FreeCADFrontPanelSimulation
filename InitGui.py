# FreeCAD init script of Front Panel Simulation module  

#***************************************************************************
#*   (c) Daniel Zicsi-Liess liessdaniel415@gmail.com 2018                  *   
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************/

import FreeCAD
import FreeCADGui


class FrontPanelSim (Workbench):
    import FPSimInit
    # __dir__ = os.path.dirname( __file__ ) # __file__ is not working
    Icon = FPSimInit.__dir__ + '/icons/WorkbenchIcon.svg'
    ToolTip = "This Workbench brings the frontpanel to life"
    MenuText = 'Frontpanel simulation'

    def Initialize(self):
        "This function is executed when FreeCAD starts"
        # import MyModuleA, MyModuleB # import here all the needed files that create your FreeCAD commands
        import FPSimInit
        self.list = ["CreateDisplay", "CreateButton"] # A list of command names created in the line above
        self.appendToolbar("My Commands",self.list) # creates a new toolbar with your commands
        self.appendMenu("My New Menu",self.list) # creates a new menu
        self.appendMenu(["An existing Menu","My submenu"],self.list) # appends a submenu to an existing menu

    def Activated(self):
        "This function is executed when the workbench is activated"
        FreeCAD.Console.PrintMessage("FrontPanelSim WB activated")
        return

    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        FreeCAD.Console.PrintMessage("FrontPanelSim WB deactivated")
        return

    def ContextMenu(self, recipient):
        "This is executed whenever the user right-clicks on screen"
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("My commands",self.list) # add commands to the context menu

    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"
       
FreeCADGui.addWorkbench(FrontPanelSim())



#    def Activated(self):
#        import ExplodedAssembly as ea
#        if not(FreeCAD.ActiveDocument):
#            FreeCAD.newDocument()

#        ea.checkDocumentStructure()
#        FreeCAD.Console.PrintMessage('Exploded Assembly workbench loaded\n')


