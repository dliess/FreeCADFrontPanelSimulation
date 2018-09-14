import FreeCAD
from PySide import QtGui
from FPWidgetTypes import FPWidgetTypes
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
                    dim = (int(match.group(2)) + 1,)

            if not label in wData:
                wData[label] = { 'Dimension' : None, 'wType' : None }
            if(dim and wData[label]['Dimension']):
                if len(dim) == 1:
                    maxDim = (max(dim[0], wData[label]['Dimension'][0]),)
                elif len(dim) == 2:
                    maxDim = (max(dim[0], wData[label]['Dimension'][0]), max(dim[1], wData[label]['Dimension'][1]))
            else:
                maxDim = dim
            wData[label]['Dimension'] = maxDim
            if not wData[label]['wType']:
                if obj.Name.find("FPSimLinearPotentiometer") == 0:
                    wData[label]['wType'] = [FPWidgetTypes.POTENTIOMETER, FPWidgetTypes.POT_MOVE]
                elif obj.Name.find("FPSimButton") == 0:
                    wData[label]['wType'] = [FPWidgetTypes.BUTTON]
                elif obj.Name.find("FPSimDisplay") == 0:
                    wData[label]['wType'] = [FPWidgetTypes.DISPLAY]
                elif obj.Name.find("FPSimRotaryEncoder") == 0:
                    wData[label]['wType'] = [FPWidgetTypes.ENCODER, FPWidgetTypes.BUTTON]
                elif obj.Name.find("FPSimRotaryPotentiometer") == 0:
                    wData[label]['wType'] = [FPWidgetTypes.POTENTIOMETER, FPWidgetTypes.POT_MOVE]
                elif obj.Name.find("FPSimLED") == 0:
                    wData[label]['wType'] = [FPWidgetTypes.LED]

    topology = []
    for label in wData:
        widget = {'Label' : label, 'Dimension' : wData[label]['Dimension'], 'WidgetType' : wData[label]['wType']}
        topology.append(widget)

    fileName = QtGui.QFileDialog.getSaveFileName(dir = "WidgetTopology.json", filter="WidgetTopology file (WidgetTopology.json)")[0]
    if len(fileName) > 0:
        with open(fileName, 'w') as outfile:
            json.dump(topology, outfile, indent=3)
