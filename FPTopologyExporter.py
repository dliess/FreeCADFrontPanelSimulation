import FreeCAD
from PySide import QtGui
from FPWidgetActionCategory import FPWidgetActionCategory
import re
import json

def exportTopology():
    wData = dict()
    for obj in FreeCAD.ActiveDocument.Objects:
        label = obj.Label
        dim = None
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

            if not label in wData:
                wData[label] = { 'Dimension' : None, 'ActionCat' : None }
            if(dim and wData[label]['Dimension']):
                maxDim = (max(dim[0], wData[label]['Dimension'][0]), max(dim[1], wData[label]['Dimension'][1]))
            else:
                maxDim = dim
            wData[label]['Dimension'] = maxDim
            if not wData[label]['ActionCat']:
                if obj.Name.find("FPSimLinearPotentiometer") == 0:
                    wData[label]['ActionCat'] = [FPWidgetActionCategory.POTENTIOMETER, FPWidgetActionCategory.POT_MOVE]
                elif obj.Name.find("FPSimButton") == 0:
                    wData[label]['ActionCat'] = [FPWidgetActionCategory.BUTTON]
                elif obj.Name.find("FPSimDisplay") == 0:
                    wData[label]['ActionCat'] = [FPWidgetActionCategory.DISPLAY]
                elif obj.Name.find("FPSimRotaryEncoder") == 0:
                    wData[label]['ActionCat'] = [FPWidgetActionCategory.ENCODER, FPWidgetActionCategory.BUTTON]
                elif obj.Name.find("FPSimRotaryPotentiometer") == 0:
                    wData[label]['ActionCat'] = [FPWidgetActionCategory.POTENTIOMETER, FPWidgetActionCategory.POT_MOVE]
                elif obj.Name.find("FPSimLED") == 0:
                    wData[label]['ActionCat'] = [FPWidgetActionCategory.LED]

    topology = []
    id = 0
    for label in wData:
        widget = {'Id' : id, 'Label' : label, 'Dimension' : wData[label]['Dimension'], 'ActionCategory' : wData[label]['ActionCat']}
        topology.append(widget)
        id = id + 1


    fileName = QtGui.QFileDialog.getSaveFileName( filter="Json file (*.json)" )[0]
    if len(fileName) > 0:
        with open(fileName, 'w') as outfile:
            json.dump(topology, outfile)
