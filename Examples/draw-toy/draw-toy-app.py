#!/usr/bin/python

from __future__ import print_function

import grpc

import generated.python.FPSimulation_pb2 as Proto
import generated.python.FPSimulation_pb2_grpc as GRPC
from time import sleep
from copy import deepcopy
import math

class Modes:
    DRAW_POINTS           = 0
    DRAW_CONNECTOR_LINES  = 1
    DRAW_LINES            = 2
    DRAW_RECTANGLES       = 3
    DRAW_RECTANGLES_FULL  = 4

def displayImage(stub):
    # 3x3 bitmap
    p1 = Proto.PixelPos(x = 5, y = 5)
    p2 = Proto.PixelPos(x = 7, y = 7)
    bitmap3x3 = [Proto.Color(r = 255, g = 0, b = 0, a = 255),
                 Proto.Color(r = 255, g = 0, b = 0, a = 255),
                 Proto.Color(r = 255, g = 0, b = 0, a = 255),
                
                 Proto.Color(r = 255, g = 0, b = 0, a = 255),
                 Proto.Color(r = 255, g = 0, b = 0, a = 255),
                 Proto.Color(r = 255, g = 0, b = 0, a = 255),

                 Proto.Color(r = 255, g = 0, b = 0, a = 255),
                 Proto.Color(r = 255, g = 0, b = 0, a = 255),
                 Proto.Color(r = 255, g = 0, b = 0, a = 255)]

    data = Proto.DisplaySubWindowData(p1 = p1, p2 = p2)
    data.pixelColor.extend(bitmap3x3)
    req = Proto.DisplaySubWindowPixelsRequest(objLabel = "FPSimDisplay", data = data)
    stub.display_setSubWindowPixels(req)

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
    colRed = 0
    colGreen = 0
    colBlue = 0
    FREQ_MAX_HZ = 30.0
    freqRedHz = 0.0
    freqGreenHz = 0.0
    freqBlueHz = 0.0
    ampRedFactor = 1.0
    ampGreenFactor = 1.0
    ampBlueFactor = 1.0
    lastEraserPotiVal = None
    mode = Modes.DRAW_POINTS
    LedOnColor = Proto.Color(r = 255, g = 0, b = 0, a = 255)
    LedOffColor = Proto.Color(r = 0, g = 0, b = 0, a = 255)
    req = Proto.LedSetColorRequest(objLabel = "Mode1Led", color = LedOnColor)
    stub.led_setColor(req)
    req = Proto.LedSetColorRequest(objLabel = "Mode2Led", color = LedOffColor)
    stub.led_setColor(req)
    req = Proto.LedSetColorRequest(objLabel = "Mode3Led", color = LedOffColor)
    stub.led_setColor(req)
    req = Proto.LedSetColorRequest(objLabel = "Mode4Led", color = LedOffColor)
    stub.led_setColor(req)
    req = Proto.LedSetColorRequest(objLabel = "Mode5Led", color = LedOffColor)
    stub.led_setColor(req)
    req = Proto.LedSetColorRequest(objLabel = "ColorModLed", color = LedOffColor)
    stub.led_setColor(req)
    font = Proto.FontData(path="truetype/ttf-bitstream-vera/VeraIt.ttf", size=40)
    req = Proto.DisplaySetActiveFontRequest(objLabel = "FPSimDisplay", data = font)
    stub.display_setActiveFont(req)
    txt = Proto.TextData(pos=Proto.PixelPos(x=10,y=10), color=Proto.Color(r=0, g=255, b=0, a=255), text="Im a draw-toy")
    req = Proto.DisplayDrawTextRequest(objLabel = "FPSimDisplay", data = txt)
    stub.display_drawText(req)

    colorAutomationOn = False
    t = 0.0
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
                    req = Proto.LedSetColorRequest(objLabel = "Mode5Led", color = LedOffColor)
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
                    req = Proto.LedSetColorRequest(objLabel = "Mode5Led", color = LedOffColor)
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
                    req = Proto.LedSetColorRequest(objLabel = "Mode5Led", color = LedOffColor)
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
                    req = Proto.LedSetColorRequest(objLabel = "Mode5Led", color = LedOffColor)
                    stub.led_setColor(req)
                    mode = Modes.DRAW_RECTANGLES
            elif button.objLabel == "Mode5Btn":
                if mode != Modes.DRAW_RECTANGLES_FULL:
                    req = Proto.LedSetColorRequest(objLabel = "Mode1Led", color = LedOffColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode2Led", color = LedOffColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode3Led", color = LedOffColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode4Led", color = LedOffColor)
                    stub.led_setColor(req)
                    req = Proto.LedSetColorRequest(objLabel = "Mode5Led", color = LedOnColor)
                    stub.led_setColor(req)
                    mode = Modes.DRAW_RECTANGLES_FULL

            elif button.objLabel == "ColorAutomationBtn":
                if button.state == Proto.BUTTON_PRESSED:
                    if colorAutomationOn:
                        colorAutomationOn = False
                        req = Proto.LedSetColorRequest(objLabel = "ColorModLed", color = LedOffColor)
                        stub.led_setColor(req)
                    else:
                        colorAutomationOn = True
                        req = Proto.LedSetColorRequest(objLabel = "ColorModLed", color = LedOnColor)
                        stub.led_setColor(req)

        for potentiometer in stub.getPotentiometerValues(Proto.Empty()):
            if potentiometer.objLabel == "PotRed":
                colRed = potentiometer.value
            if potentiometer.objLabel == "PotGreen":
                colGreen = potentiometer.value
            if potentiometer.objLabel == "PotBlue":
                colBlue = potentiometer.value
            if potentiometer.objLabel == "PotEraser":
                if not lastEraserPotiVal:
                    lastEraserPotiVal = potentiometer.value
                if lastEraserPotiVal != potentiometer.value:
                    pixColor = Proto.Color(r = 0, g = 0, b = 0, a=255)
                    X1 = int(float(lastEraserPotiVal * resolution.x) / 1024.0)
                    X2 = int(float(potentiometer.value * resolution.x) / 1024.0)
                    P1 = Proto.PixelPos( x = X1, y = 0 )
                    P2 = Proto.PixelPos( x = X2, y = resolution.y - 1)
                    rectData = Proto.RectangleData(p1 = P1, p2 = P2, pixelColor = pixColor, filled = True)
                    req = Proto.DisplayDrawRectangleRequest(objLabel = "FPSimDisplay", data = rectData)
                    stub.display_drawRectangle(req)
                    lastEraserPotiVal = potentiometer.value
            if potentiometer.objLabel == "PotFreqRed":
                freqRedHz = (potentiometer.value * FREQ_MAX_HZ) / 64.0
            if potentiometer.objLabel == "PotFreqGreen":
                freqGreenHz = (potentiometer.value * FREQ_MAX_HZ) / 64.0
            if potentiometer.objLabel == "PotFreqBlue":
                freqBlueHz = (potentiometer.value * FREQ_MAX_HZ) / 64.0


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
                if touchValueAnswer.pos.x != -1:
                    pixPos1.x = touchValueAnswer.pos.x
                    pixPos1.y = touchValueAnswer.pos.y
                    cursorChanged = True
            if touchValueAnswer.objLabel == "AmpRedTouch":
                if touchValueAnswer.pos.x != -1:
                    ampRedFactor = touchValueAnswer.pos.x  / 100.0
            if touchValueAnswer.objLabel == "AmpGreenTouch":
                if touchValueAnswer.pos.x != -1:
                    ampGreenFactor = touchValueAnswer.pos.x  / 100.0
            if touchValueAnswer.objLabel == "AmpBlueTouch":
                if touchValueAnswer.pos.x != -1:
                    ampBlueFactor = touchValueAnswer.pos.x  / 100.0

        if colorAutomationOn:
            if freqRedHz > 0.0 and ampRedFactor > 0.0:
                req = Proto.MovePotentiometerRequest(objLabel = "PotRed", value = int(((math.sin(t*freqRedHz) * ampRedFactor + 1.0)  / 2.0) * 255.0))
                stub.movePotentiometerToValue(req)
            if freqGreenHz > 0.0 and ampGreenFactor > 0.0:
                req = Proto.MovePotentiometerRequest(objLabel = "PotGreen", value = int(((math.sin(t*freqGreenHz) * ampGreenFactor + 1.0)  / 2.0) * 255.0))
                stub.movePotentiometerToValue(req)
            if freqBlueHz > 0.0 and ampBlueFactor > 0.0:
                req = Proto.MovePotentiometerRequest(objLabel = "PotBlue", value = int(((math.sin(t*freqBlueHz) * ampBlueFactor  + 1.0) / 2.0) * 255.0))
                stub.movePotentiometerToValue(req)

        if cursorChanged:
            cursorChanged = False
            pixColor = Proto.Color(r = colRed, g = colGreen, b = colBlue, a = 255)
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
                rectData = Proto.RectangleData(p1 = pixPos1, p2 = pixPos2, pixelColor = pixColor, filled = False)
                req = Proto.DisplayDrawRectangleRequest(objLabel = "FPSimDisplay", data = rectData)
                stub.display_drawRectangle(req)
            elif mode == Modes.DRAW_RECTANGLES_FULL:
                rectData = Proto.RectangleData(p1 = pixPos1, p2 = pixPos2, pixelColor = pixColor, filled = True)
                req = Proto.DisplayDrawRectangleRequest(objLabel = "FPSimDisplay", data = rectData)
                stub.display_drawRectangle(req) 
            prevPixPos1 = deepcopy(pixPos1)
            prevPixPos2 = deepcopy(pixPos2)
        if colorAutomationOn:
            t = t + 0.01
        sleep(0.01)



if __name__ == '__main__':
    run()
