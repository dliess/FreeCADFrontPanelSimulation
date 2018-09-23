import FreeCAD
from PySide import QtGui

import re
import json

def _extractLabelAndDim(obj):
    label = obj.Label
    dim = None
    match = re.match("(.*)\[(\d+)\]\[(\d+)\]", obj.Label)
    if match:
        label = match.group(1)
        dim = (int(match.group(2)) + 1, int(match.group(3)) + 1)
    else: 
        match = re.match("(.*)\[(\d+)\]", obj.Label)
        if match:
            label = match.group(1)
            dim = (int(match.group(2)) + 1,)
    return (label, dim)

def _getWidgetTopology():
    wData = dict()
    for obj in FreeCAD.ActiveDocument.Objects:
        if obj.Name.find("FPSim") == 0:
            (label, dim) = _extractLabelAndDim(obj)

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
                    wData[label]['wType'] = ["Potentiometer"]
                    if obj.Motorized:
                        wData[label]['wType'].append("Motor")
                    if not 'PotentiometerResolution' in wData[label]:
                        wData[label]['PotentiometerResolution'] = obj.Resolution
                elif obj.Name.find("FPSimButton") == 0:
                    wData[label]['wType'] = ["Button"]
                elif obj.Name.find("FPSimDisplay") == 0:
                    wData[label]['wType'] = ["Display"]
                    if not 'DisplayResolution' in wData[label]:
                        wData[label]['DisplayResolution'] = {'ResolutionX' : obj.ResolutionX, 'ResolutionY' : obj.ResolutionY}
                elif obj.Name.find("FPSimRotaryEncoder") == 0:
                    wData[label]['wType'] = ["Encoder"]
                    if obj.PushButton:
                        wData[label]['wType'].append("Button")
                elif obj.Name.find("FPSimRotaryPotentiometer") == 0:
                    wData[label]['wType'] = ["Potentiometer"]
                    if obj.Motorized:
                        wData[label]['wType'].append("Motor")
                    if not 'PotentiometerResolution' in wData[label]:
                        wData[label]['PotentiometerResolution'] = obj.IncrementsOnWholeArc
                elif obj.Name.find("FPSimLED") == 0:
                    wData[label]['wType'] = ["Led"]
                elif obj.Name.find("FPSimTouchSurface") == 0:
                    wData[label]['wType'] = ["TouchSurface"]
                    if not 'TouchSurfaceResolution' in wData[label]:
                        wData[label]['TouchSurfaceResolution'] = {'ResolutionX' : obj.ResolutionX, 'ResolutionY' : obj.ResolutionY}

    topology = []
    for label in wData:
        widget = {'Label' : label, 'Dimension' : wData[label]['Dimension'], 'WidgetType' : wData[label]['wType']}
        if "Potentiometer" in wData[label]['wType']:
            widget['PotentiometerResolution'] = wData[label]['PotentiometerResolution']
        if "Display" in wData[label]['wType']:
            widget['DisplayResolution'] = wData[label]['DisplayResolution']
        if "TouchSurface" in wData[label]['wType']:
            widget['TouchSurfaceResolution'] = wData[label]['TouchSurfaceResolution']
        topology.append(widget)
    
    return topology

def exportWidgetInfo():
    saveDir = None
    saveDir = QtGui.QFileDialog.getExistingDirectory()
    if not saveDir:
        return

    topologyFileName = saveDir + "/WidgetTopology.json"

    topology = _getWidgetTopology()

    if len(topologyFileName) > 0:
        with open(topologyFileName, 'w') as outfile:
            json.dump(topology, outfile, indent=3)

