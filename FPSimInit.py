# -*- coding: utf-8 -*-
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
import os

__dir__ = os.path.dirname(__file__)


class CreateDisplay:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/CreateDisplay.svg',
                'MenuText': 'Create Display',
                'ToolTip': 'Create a special exploded group for screws, nuts, bolts... \n Select circular edges of the shape you want to animate, then\n select one face (arbitrary shape) wich has as normal vector\nin the direction in wich you want to move the selected shapes'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        FreeCAD.Console.PrintMessage("CreateDisplay activated");


class CreateButton:
    def GetResources(self):
        return {'Pixmap': __dir__ + '/icons/CreateButton.svg',
                'MenuText': 'Create Button',
                'ToolTip': 'Select the objects you want to explode and\nfinally the face which its normal is the trajectory director vector'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        FreeCAD.Console.PrintMessage("CreateButton activated");


FreeCAD.Gui.addCommand('CreateDisplay', CreateDisplay())
FreeCAD.Gui.addCommand('CreateButton', CreateButton())