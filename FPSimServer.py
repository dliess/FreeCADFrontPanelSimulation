
from concurrent import futures
from PySide import QtCore
import grpc
import generated.python.FPSimulation_pb2 as Proto
import generated.python.FPSimulation_pb2_grpc as GRPC
from threading import Lock
import FreeCAD
import FPSimDisplay

import time

class DataAquisitionCBHolder:
    def __init__(self):
        # TODO: check if this lock is really necessary
        # for multithreaded dictionary access in python 
        self._mutex = Lock()
        self.buttonCB = {}
        self.encoderCB = {}
        self.potentiometerCB = {}
        self.touchSurfaceCB = {}


    def setButtonCB(self, objName, cb):
        self._mutex.acquire()
        try:
            self.buttonCB[objName] = cb
        finally:
            self._mutex.release()
    
    def clearButtonCB(self, objName):
        self._mutex.acquire()
        try:
            self.buttonCB[objName] = None
        finally:
            self._mutex.release()

    def setEncoderCB(self, objName, cb):
        self._mutex.acquire()
        try:
            self.encoderCB[objName] = cb
        finally:
            self._mutex.release()
    
    def clearEncoderCB(self, objName):
        self._mutex.acquire()
        try:
            self.encoderCB[objName] = None
        finally:
            self._mutex.release()

    def setPotentiometerCB(self, objName, cb):
        self._mutex.acquire()
        try:
            self.potentiometerCB[objName] = cb
        finally:
            self._mutex.release()
    
    def clearPotentiometerCB(self, objName):
        self._mutex.acquire()
        try:
            self.potentiometerCB[objName] = None
        finally:
            self._mutex.release()

    def setTouchSurfaceCB(self, objName, cb):
        self._mutex.acquire()
        try:
            self.touchSurfaceCB[objName] = cb
        finally:
            self._mutex.release()
    
    def clearTouchSurfaceCB(self, objName):
        self._mutex.acquire()
        try:
            self.touchSurfaceCB[objName] = None
        finally:
            self._mutex.release()
    
dataAquisitionCBHolder = DataAquisitionCBHolder()
_commandedValues = dict()


class FPSimulationService(GRPC.FPSimulationServicer):
    def led_setColor(self, request, context):
        try:
            obj = FreeCAD.ActiveDocument.getObjectsByLabel(request.objLabel)[0]
            obj.Proxy.setColor(obj, request.color)
        except IndexError:
            FreeCAD.Console.PrintError(
                "Object not found with label " + request.objLabel + "\n")
        return Proto.Empty()

    def display_setPixels_ARGB32(self, request, context):
        try:
            start = time.time()
            obj = FreeCAD.ActiveDocument.getObjectsByLabel(request.objLabel)[0]
            obj.Proxy.setPixels_ARGB32(obj, request.pixelDataList)
            durationUs = int((time.time() - start) * 1000000)
        except IndexError:
            FreeCAD.Console.PrintError(
                "Object not found with label " + request.objLabel + "\n")
        answ = Proto.Duration(usec = durationUs)
        return answ


    def display_setSubWindowPixels_ARGB32(self, request, context):
        try:
            start = time.time()
            obj = FreeCAD.ActiveDocument.getObjectsByLabel(request.objLabel)[0]
            obj.Proxy.setSubWindowPixels_ARGB32(obj, request.data)
            durationUs = int((time.time() - start) * 1000000)
        except IndexError:
            FreeCAD.Console.PrintError(
                "Object not found with label " + request.objLabel + "\n")
        answ = Proto.Duration(usec = durationUs)
        return answ


    def display_drawRectangle(self, request, context):
        try:
            obj = FreeCAD.ActiveDocument.getObjectsByLabel(request.objLabel)[0]
            obj.Proxy.drawRectangle(obj, request.data)
        except IndexError:
            FreeCAD.Console.PrintError(
                "Object not found with label " + request.objLabel + "\n")
        return Proto.Empty()

    def display_drawLine(self, request, context):
        try:
            obj = FreeCAD.ActiveDocument.getObjectsByLabel(request.objLabel)[0]
            obj.Proxy.drawLine(obj, request.data)
        except IndexError:
            FreeCAD.Console.PrintError(
                "Object not found with label " + request.objLabel + "\n")
        return Proto.Empty()

    def display_setActiveFont(self, request, context):
        try:
            obj = FreeCAD.ActiveDocument.getObjectsByLabel(request.objLabel)[0]
            obj.Proxy.setActiveFont(obj, request.data)
        except IndexError:
            FreeCAD.Console.PrintError(
                "Object not found with label " + request.objLabel + "\n")
        return Proto.Empty()

    def display_drawText(self, request, context):
        try:
            obj = FreeCAD.ActiveDocument.getObjectsByLabel(request.objLabel)[0]
            obj.Proxy.drawText(obj, request.data)
        except IndexError:
            FreeCAD.Console.PrintError(
                "Object not found with label " + request.objLabel + "\n")
        return Proto.Empty()

    def display_getResolution(self, request, context):
        try:
            obj = FreeCAD.ActiveDocument.getObjectsByLabel(request.objLabel)[0]
            return obj.Proxy.getResolution(obj)
        except IndexError:
            FreeCAD.Console.PrintError(
                "Object not found with label " + request.objLabel + "\n")
            answ = Proto.DisplayResolutionAnswer(x = 0, y = 0)
            return answ

    def display_clearDisplay(self, request, context):
        try:
            obj = FreeCAD.ActiveDocument.getObjectsByLabel(request.objLabel)[0]
            obj.Proxy.clearDisplay(obj, color = None)
        except IndexError:
            FreeCAD.Console.PrintError(
                "Object not found with label " + request.objLabel + "\n")
        return Proto.Empty()   

    def display_getTextSize(self, request, context):
        try:
            obj = FreeCAD.ActiveDocument.getObjectsByLabel(request.objLabel)[0]
            return obj.Proxy.getTextSize(obj, request.text, request.fontData )
        except IndexError:
            FreeCAD.Console.PrintError(
                "Object not found with label " + request.objLabel + "\n")
            answ = Proto.DisplayGetTextSizeAnswer(w = 0, h = 0)
            return answ
   
    def getButtonStates(self, request, context):
        for objName in dataAquisitionCBHolder.buttonCB:
            if(dataAquisitionCBHolder.buttonCB[objName]):
                obj = FreeCAD.ActiveDocument.getObject(objName)
                answ = Proto.GetButtonStateAnswer()
                answ.objLabel = obj.Label
                answ.state = dataAquisitionCBHolder.buttonCB[objName](objName) 
                yield answ

    def getButton3dStates(self, request, context):
        for objName in dataAquisitionCBHolder.buttonCB:
            if(dataAquisitionCBHolder.buttonCB[objName]):
                obj = FreeCAD.ActiveDocument.getObject(objName)
                answ = Proto.GetButtonStateAnswer()
                answ.objLabel = obj.Label
                answ.state = dataAquisitionCBHolder.buttonCB[objName](objName) 
                yield answ

    def getButton5dStates(self, request, context):
        for objName in dataAquisitionCBHolder.buttonCB:
            if(dataAquisitionCBHolder.buttonCB[objName]):
                obj = FreeCAD.ActiveDocument.getObject(objName)
                answ = Proto.GetButtonStateAnswer()
                answ.objLabel = obj.Label
                answ.state = dataAquisitionCBHolder.buttonCB[objName](objName) 
                yield answ

    def getEncoderIncrements(self, request, context):
        for objName in dataAquisitionCBHolder.encoderCB:
            if(dataAquisitionCBHolder.encoderCB[objName]):
                obj = FreeCAD.ActiveDocument.getObject(objName)
                answ = Proto.GetEncoderIncrementsAnswer()
                answ.objLabel = obj.Label
                answ.increments = dataAquisitionCBHolder.encoderCB[objName](objName) 
                yield answ

    def getPotentiometerValues(self, request, context):
        for objName in dataAquisitionCBHolder.potentiometerCB:
            if(dataAquisitionCBHolder.potentiometerCB[objName]):
                obj = FreeCAD.ActiveDocument.getObject(objName)
                answ = Proto.GetPotentiometerValuesAnswer()
                answ.objLabel = obj.Label
                answ.value = dataAquisitionCBHolder.potentiometerCB[objName](objName) 
                yield answ

    def movePotentiometerToValue(self, request, context):
        try:
            obj = FreeCAD.ActiveDocument.getObjectsByLabel(request.objLabel)[0]
            _commandedValues[obj.Name] = request.value
        except IndexError:
            FreeCAD.Console.PrintError(
                "Object not found with label " + request.objLabel + "\n")
        return Proto.Empty()
        

    def getTouchValue(self, request, context):
        for objName in dataAquisitionCBHolder.touchSurfaceCB:
            if(dataAquisitionCBHolder.touchSurfaceCB[objName]):
                obj = FreeCAD.ActiveDocument.getObject(objName)
                answ = Proto.GetTouchValueAnswer()
                answ.objLabel = obj.Label
                tup = dataAquisitionCBHolder.touchSurfaceCB[objName](objName)
                answ.pos.x = tup[0]
                answ.pos.y = tup[1]                  
                yield answ

import math
class Server:
    def __init__(self):
        self._server = None
        self._timer = QtCore.QTimer()
        QtCore.QObject.connect(self._timer, QtCore.SIGNAL("timeout()"), self.appRecompute)

    def start(self, port = 50051): 
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        GRPC.add_FPSimulationServicer_to_server(FPSimulationService(), self._server)
        self._server.add_insecure_port('[::]:' + str(port))
        self._server.start()
        self._timer.start(33)

    def stop(self):
        self._server.stop(0)
        del self._server
        self._timer.stop()

    def appRecompute(self):
        for objName in _commandedValues.keys():
            obj = FreeCAD.ActiveDocument.getObject(objName)
            obj.Proxy.moveToValue(objName, _commandedValues[objName])
            del  _commandedValues[objName]
        FPSimDisplay.updateObjectTexture()
        #FreeCAD.ActiveDocument.recompute()

server = Server()
