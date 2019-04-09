import FreeCAD
from PySide import QtGui

import re
import json

def _extractLabelAndIndexes(obj):
    label = obj.Label
    indexes = None
    match = re.match("(.*)\[(\d+)\]\[(\d+)\]", obj.Label)
    if match:
        label = match.group(1)
        indexes = (int(match.group(2)), int(match.group(3)))
    else: 
        match = re.match("(.*)\[(\d+)\]", obj.Label)
        if match:
            label = match.group(1)
            indexes = (int(match.group(2)),)
    return (label, indexes)

def _determineDimensions():
    dims = dict()
    for obj in FreeCAD.ActiveDocument.Objects:
        if obj.Name.find("FPSim") == 0:
            (label, indexes) = _extractLabelAndIndexes(obj)
            if (not indexes) or (not label in dims):
                dims[label] = (1,1)
            elif len(indexes) == 1:
                    dims[label] = (max(indexes[0] + 1, dims[label][0]), 1)
            elif len(indexes) == 2:
                dims[label] = (max(indexes[0] + 1, dims[label][0]), max(indexes[1] + 1, dims[label][1]))
    return dims

def _isFirstIndexInArray(indexes):
    if not indexes:
        return True
    elif len(indexes) == 1:
        return indexes == (0,)
    elif len(indexes) == 2:
        return indexes == (0,0)

def _initWData():
    wData = dict()
    wData['Potentiometer'] = dict()
    wData['Button'] = dict()
    wData['Button3d'] = dict()
    wData['Button5d'] = dict()
    wData['Encoder'] = dict()
    wData['TouchSurface'] = dict()
    wData['Display'] = dict()
    wData['Led'] = dict()
    wData['Positioner'] = dict()
    return wData


def _has5dButtonTraits(buttonObj):
    return hasattr(buttonObj, 'PressureResolutionLin') and \
           (buttonObj.PressureResolutionLin.x != 0 or buttonObj.PressureResolutionLin.y != 0)

def _has3dButtonTraits(buttonObj):
    return (hasattr(buttonObj, 'PressureResolutionLin') and (buttonObj.PressureResolutionLin.z != 0)) or \
           (hasattr(buttonObj, 'VelocityResolution')    and (buttonObj.VelocityResolution != 0))

def _collectData():
    wData = _initWData()
    dimensions = _determineDimensions()
    for obj in FreeCAD.ActiveDocument.Objects:
        if obj.Name.find("FPSim") == 0:
            (label, indexes) = _extractLabelAndIndexes(obj)
            if not _isFirstIndexInArray(indexes):
                continue

            if obj.Name.find("FPSimLinearPotentiometer") == 0:
                wData['Potentiometer'][label] = { 'Dimension' : dimensions[label], 'Resolution' : obj.Resolution }
                if hasattr(obj, 'Motorized') and obj.Motorized:
                    wData['Positioner'][label] = { 'Dimension' : dimensions[label], 'Resolution' : obj.Resolution }

            elif obj.Name.find("FPSimButton") == 0:
                if _has5dButtonTraits(obj):
                    if hasattr(obj, 'PressureResolutionLin'):
                        wData['Button5d'][label] = { 'Dimension' : dimensions[label], 'Resolution' : \
                            { 'Velocity' : 0 ,\
                              'Pressure' : (obj.PressureResolutionLin.x, \
                                            obj.PressureResolutionLin.y, \
                                            obj.PressureResolutionLin.z)} }
                    if hasattr(obj, 'VelocityResolution'):
                        wData['Button5d'][label]['Resolution']['Velocity'] = obj.VelocityResolution
                elif _has3dButtonTraits(obj):
                    wData['Button3d'][label] = { 'Dimension' : dimensions[label],\
                                               'Resolution' : { 'Velocity' : 0, 'Pressure' : 0  } }
                    if hasattr(obj, 'PressureResolutionLin'):
                        wData['Button3d'][label]['Resolution']['Velocity'] = obj.PressureResolutionLin.z
                    if hasattr(obj, 'VelocityResolution'):
                        wData['Button3d'][label]['Resolution']['Velocity'] = obj.VelocityResolution
                else:
                    wData['Button'][label] = { 'Dimension' : dimensions[label] }

            elif obj.Name.find("FPSimDisplay") == 0:
                wData['Display'][label] = { 'Dimension' : dimensions[label], 'Resolution' : (obj.ResolutionX, obj.ResolutionY) }

            elif obj.Name.find("FPSimRotaryEncoder") == 0:
                wData['Encoder'][label] = { 'Dimension' : dimensions[label] } # TODO Resolution?
                if hasattr(obj, 'PushButton') and obj.PushButton:
                    wData['Button'][label] = { 'Dimension' : dimensions[label] }

            elif obj.Name.find("FPSimRotaryPotentiometer") == 0:
                wData['Potentiometer'][label] = { 'Dimension' : dimensions[label], 'Resolution' : obj.IncrementsOnWholeArc }
                if hasattr(obj, 'Motorized') and obj.Motorized:
                    wData['Positioner'][label] = { 'Dimension' : dimensions[label], 'Resolution' : obj.IncrementsOnWholeArc }

            elif obj.Name.find("FPSimLED") == 0:
                wData['Led'][label] = { 'Dimension' : dimensions[label] }

            elif obj.Name.find("FPSimTouchSurface") == 0:
                wData['TouchSurface'][label] = { 'Dimension' : dimensions[label], 'Resolution' : (obj.ResolutionX, obj.ResolutionY) }

    return wData

def exportWidgetInfo(documentName):
    saveDir = None
    saveDir = QtGui.QFileDialog.getExistingDirectory()
    if not saveDir:
        return

    topologyFileName = saveDir + "/" + documentName + "Topology.json"

    topology = _collectData()

    if len(topologyFileName) > 0:
        with open(topologyFileName, 'w') as outfile:
            json.dump(topology, outfile, indent=3)

