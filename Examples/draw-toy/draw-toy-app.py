#!/usr/bin/python

from __future__ import print_function

import grpc

import generated.FPSimulation_pb2 as Proto
import generated.FPSimulation_pb2_grpc as GRPC
from time import sleep
from copy import deepcopy

class Modes:
    DRAW_POINTS           = 0
    DRAW_CONNECTOR_LINES  = 1
    DRAW_LINES            = 2
    DRAW_RECTANGLES       = 3

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = GRPC.FPSimulationStub(channel)
    cursorChanged = False
    resReq = Proto.DisplayResolutionRequest(objLabel = "FPSimDisplay")
    resolution = stub.display_getResolution(resReq)
    pixPos1 = Proto.PixelPos(x = resolution.x / 2, y = resolution.y / 2)
    pixPos2 = Proto.PixelPos(x = resolution.x / 2, y = resolution.y / 2)
    prevPixPos1 = deepcopy(pixPos1)
    prevPixPos2 = deepcopy(pixPos2)
    colRed = 0.0
    colGreen = 0.0
    colBlue = 0.0
    lastEraserPotiVal = None
    mode = Modes.DRAW_POINTS
    LedOnColor = Proto.ColorRGB(red = 1.0, green = 0.0, blue = 0.0)
    LedOffColor = Proto.ColorRGB(red = 0.0, green = 0.0, blue = 0.0)
    req = Proto.LedSetColorRequest(objLabel = "Mode1Led", color = LedOnColor)
    stub.led_setColor(req)
    req = Proto.LedSetColorRequest(objLabel = "Mode2Led", color = LedOffColor)
    stub.led_setColor(req)
    req = Proto.LedSetColorRequest(objLabel = "Mode3Led", color = LedOffColor)
    stub.led_setColor(req)
    req = Proto.LedSetColorRequest(objLabel = "Mode4Led", color = LedOffColor)
    stub.led_setColor(req)
    while True:
        for button in stub.getButtonStates(Proto.Empty()):
            if button.objLabel == "Mode1Btn":
                if mode != Modes.DRAW_POINTS:
                    req = Proto.LedSetColorRequest(objLabel = "Mode1Led", color = LedOnColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode2Led", color = LedOffColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode3Led", color = LedOffColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode4Led", color = LedOffColor)
                    stub.led_setColor(req)
                    mode = Modes.DRAW_POINTS
            elif button.objLabel == "Mode2Btn":
                if mode != Modes.DRAW_CONNECTOR_LINES:
                    req = Proto.LedSetColorRequest(objLabel = "Mode1Led", color = LedOffColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode2Led", color = LedOnColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode3Led", color = LedOffColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode4Led", color = LedOffColor)
                    stub.led_setColor(req)
                    mode = Modes.DRAW_CONNECTOR_LINES
            elif button.objLabel == "Mode3Btn":
                if mode != Modes.DRAW_LINES:
                    req = Proto.LedSetColorRequest(objLabel = "Mode1Led", color = LedOffColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode2Led", color = LedOffColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode3Led", color = LedOnColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode4Led", color = LedOffColor)
                    stub.led_setColor(req)
                    mode = Modes.DRAW_LINES
            elif button.objLabel == "Mode4Btn":
                if mode != Modes.DRAW_RECTANGLES:
                    req = Proto.LedSetColorRequest(objLabel = "Mode1Led", color = LedOffColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode2Led", color = LedOffColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode3Led", color = LedOffColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode4Led", color = LedOnColor)
                    stub.led_setColor(req)
                    mode = Modes.DRAW_RECTANGLES

        for potentiometer in stub.getPotentiometerValues(Proto.Empty()):
            if potentiometer.objLabel == "PotRed":
                colRed = potentiometer.value / 255.0
            if potentiometer.objLabel == "PotGreen":
                colGreen = potentiometer.value / 255.0
            if potentiometer.objLabel == "PotBlue":
                colBlue = potentiometer.value / 255.0
            if potentiometer.objLabel == "PotEraser":
                if not lastEraserPotiVal:
                    lastEraserPotiVal = potentiometer.value
                if lastEraserPotiVal != potentiometer.value:
                    pixColor = Proto.ColorRGB(red = 0.0, green = 0.0, blue = 0.0)
                    X1 = int(float(lastEraserPotiVal * resolution.x) / 1024.0)
                    X2 = int(float(potentiometer.value * resolution.x) / 1024.0)
                    P1 = Proto.PixelPos( x = X1, y = 0 )
                    P2 = Proto.PixelPos( x = X2, y = resolution.y - 1)
                    rectData = Proto.RectangleData(p1 = P1, p2 = P2, pixelColor = pixColor, filled = True)
                    req = Proto.DisplayDrawRectangleRequest(objLabel = "FPSimDisplay", data = rectData)
                    stub.display_drawRectangle(req)
                    lastEraserPotiVal = potentiometer.value

        for encoderIncrementsAnswer in stub.getEncoderIncrements(Proto.Empty()):
            if encoderIncrementsAnswer.objLabel == "X_POS1":
                pixPos1.x += encoderIncrementsAnswer.increments
                if pixPos1.x < 0:
                   pixPos1.x = 0
                if pixPos1.x > resolution.x - 1:
                   pixPos1.x = resolution.x - 1
                cursorChanged = True
            elif encoderIncrementsAnswer.objLabel == "Y_POS1":
                pixPos1.y += encoderIncrementsAnswer.increments
                if pixPos1.y < 0:
                   pixPos1.y = 0
                if pixPos1.y > resolution.y - 1:
                   pixPos1.y = resolution.y - 1
                cursorChanged = True
            elif encoderIncrementsAnswer.objLabel == "X_POS2":
                pixPos2.x += encoderIncrementsAnswer.increments
                if pixPos2.x < 0:
                   pixPos2.x = 0
                if pixPos2.x > resolution.x - 1:
                   pixPos2.x = resolution.x - 1
                cursorChanged = True
            elif encoderIncrementsAnswer.objLabel == "Y_POS2":
                pixPos2.y += encoderIncrementsAnswer.increments
                if pixPos2.y < 0:
                   pixPos2.y = 0
                if pixPos2.y > resolution.y - 1:
                   pixPos2.y = resolution.y - 1
                cursorChanged = True

        for touchValueAnswer in stub.getTouchValue(Proto.Empty()):
            if touchValueAnswer.objLabel == "TouchSurface":
                pixPos1.x = touchValueAnswer.pos.x
                pixPos1.y = touchValueAnswer.pos.y
                cursorChanged = True

        if cursorChanged:
            cursorChanged = False
            pixColor = Proto.ColorRGB(red = colRed, green = colGreen, blue = colBlue)
            if mode == Modes.DRAW_POINTS:
                pix1 = Proto.PixelData(pos = pixPos1, color = pixColor)
                pix2 = Proto.PixelData(pos = pixPos2, color = pixColor)
                pixDataList = Proto.PixelDataList()
                pixDataList.pixelData.extend([pix1])
                pixDataList.pixelData.extend([pix2])
                req = Proto.DisplaySetPixelsRequest(objLabel = "FPSimDisplay", pixelDataList = pixDataList)
                stub.display_setPixels(req)
            elif mode == Modes.DRAW_CONNECTOR_LINES:
                lineData1 = Proto.LineData(p1 = prevPixPos1, p2 = pixPos1, pixelColor = pixColor)
                lineData2 = Proto.LineData(p1 = prevPixPos2, p2 = pixPos2, pixelColor = pixColor)
                req = Proto.DisplayDrawLineRequest(objLabel = "FPSimDisplay", data = lineData1)
                stub.display_drawLine(req) 
                req = Proto.DisplayDrawLineRequest(objLabel = "FPSimDisplay", data = lineData2)
                stub.display_drawLine(req) 
            elif mode == Modes.DRAW_LINES:
                lineData = Proto.LineData(p1 = pixPos1, p2 = pixPos2, pixelColor = pixColor)
                req = Proto.DisplayDrawLineRequest(objLabel = "FPSimDisplay", data = lineData)
                stub.display_drawLine(req) 
            elif mode == Modes.DRAW_RECTANGLES:
                rectData = Proto.RectangleData(p1 = pixPos1, p2 = pixPos2, pixelColor = pixColor, filled = True)
                req = Proto.DisplayDrawRectangleRequest(objLabel = "FPSimDisplay", data = rectData)
                stub.display_drawRectangle(req) 
            prevPixPos1 = deepcopy(pixPos1)
            prevPixPos2 = deepcopy(pixPos2)
        sleep(0.01)



if __name__ == '__main__':
    run()
