import grpc
import generated.FPSimulation_pb2 as Proto
import generated.FPSimulation_pb2_grpc as GRPC
import re

BUTTON_PRESSED = Proto.BUTTON_PRESSED
BUTTON_RELEASED = Proto.BUTTON_RELEASED

class FpOutputs:
    def __init__(self, grpcChannel, id2LabelMap):
        self.stub = grpcChannel.stub
        self.id2LabelMap = id2LabelMap

    def setLedColor(self, widgetId, color):
        label = self.id2LabelMap.widgetIdToLabel(widgetId)
        req = Proto.LedSetColorRequest(objLabel = label, color = color)
        self.stub.led_setColor(req)
        
    def setPotentiometerMoveToValue(self, widgetId, value):
        label = self.id2LabelMap.widgetIdToLabel(widgetId)
        req = Proto.MovePotentiometerRequest(objLabel = label, value = value))
        self.stub.movePotentiometerToValue(req)

    def drawDisplayPixels(self, widgetId, pixels):
        label = self.id2LabelMap.widgetIdToLabel(widgetId)
        req = Proto.DisplaySetPixelsRequest(objLabel = label, pixelDataList = pixels)
        self.stub.display_setPixels(req)

    def drawLine(self, widgetId, line):
        label = self.id2LabelMap.widgetIdToLabel(widgetId)
        req = Proto.DisplayDrawLineRequest(objLabel = label, data = line)
        self.stub.display_drawLine(req)

    def drawRectangle(self, widgetId, rectangle):
        label = self.id2LabelMap.widgetIdToLabel(widgetId)
        req = Proto.DisplayDrawRectangleRequest(objLabel = label, data = rectangle)
        self.stub.display_drawRectangle(req)

    def setActiveFont(self, widgetId, font):
        label = self.id2LabelMap.widgetIdToLabel(widgetId)
        req = Proto.DisplaySetActiveFontRequest(objLabel = label, data = font)
        self.stub.display_setActiveFont(req)

    def drawText(self, widgetId, txt):
        label = self.id2LabelMap.widgetIdToLabel(widgetId)
        req = Proto.DisplayDrawTextRequest(objLabel = label, data = txt)
        self.stub.display_drawText(req)