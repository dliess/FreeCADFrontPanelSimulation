import FreeCAD
from PySide import QtGui
import re
import json


def exportTopology():
    topology = dict()
    for obj in FreeCAD.ActiveDocument.Objects:
        # "FPSimLinearPotentiometer", "FPSimButton", "FPSimDisplay", "FPSimRotaryEncoder", "FPSimRotaryPotentiometer", "FPSimLED"
        label = obj.Label
        dim = (1,1)
        if obj.Name.find("FPSim") == 0:
            match = re.match("(.*)\[(\d+)\]\[(\d+)\]", obj.Label)
            if match:
                label = match.group(1)
                dim = (int(match.group(2)) + 1, int(match.group(3)) + 1)
            else: 
                match = re.match("(.*)\[(\d+)\]", obj.Label)
                if match:
                    label = match.group(1)
                    dim = (int(match.group(2)) + 1, 1)
            if(label in topology):
                maxDim = (max(dim[0], topology[label][0]), max(dim[1], topology[label][1]))
            else:
                maxDim = dim
            topology[label] = maxDim


    fileName = QtGui.QFileDialog.getSaveFileName( filter="Json file (*.json)" )[0]
    if len(fileName) > 0:
        with open(fileName, 'w') as outfile:
            json.dump(topology, outfile)