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
    started = False
    i = 0
    for y in range(16):
        color = Proto.ColorRGB(red = 0.0, green = 0.0, blue = 0.0)
        req = Proto.LedSetColorRequest(objLabel = "DigitastLed00"+str(y), color = color)
        stub.led_setColor(req)

    
    while True:
        for button in stub.getButtonStates(Proto.Empty()):
            if button.objLabel == "StartBtn":
                started = True
            elif button.objLabel == "StopBtn":
                started = False

        if started:
            color = Proto.ColorRGB(red = 1.0, green = 0.0, blue = 0.0)
            req = Proto.LedSetColorRequest(objLabel = "DigitastLed00"+str(i), color = color)
            stub.led_setColor(req)
            i = i + 1
            i = i % 16

        sleep(1)



if __name__ == '__main__':
    run()
