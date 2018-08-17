import grpc
import generated.FPSimulation_pb2 as Proto
import generated.FPSimulation_pb2_grpc as GRPC
import re

#channel = grpc.insecure_channel('localhost:50051')
#self.stub = GRPC.FPSimulationStub(channel)

BUTTON_PRESSED = Proto.BUTTON_PRESSED
BUTTON_RELEASED = Proto.BUTTON_RELEASED


class FpInputs:
    def __init__(self, grpcChannel, label2IdMap):
        self.stub = grpcChannel.stub
        self.label2IdMap = label2IdMap

    def getButtonStates():
        ret = []
        for answer in self.stub.getButtonStates(Proto.Empty()):
            widgetId = self.label2IdMap.widgetLabelToId(answer.objLabel)
            state = answer.state
            ret.append({'widgetId' : widgetId, 'state' : state})
        return ret
    def getPotentiometerValues():
        ret = []
        for answer in self.stub.getPotentiometerValues(Proto.Empty()):
            widgetId = self.label2IdMap.widgetLabelToId(answer.objLabel)
            value = answer.value
            ret.append({'widgetId' : widgetId, 'value' : value})
        return ret
    def getTouchValues():
        ret = []
        for answer in self.stub.getTouchValues(Proto.Empty()):
            widgetId = self.label2IdMap.widgetLabelToId(answer.objLabel)
            pos = (answer.pos.x, answer.pos.y)
            ret.append({'widgetId' : widgetId, 'pos' : pos})
        return ret
    def getEncoderIncrements():
        ret = []
        for answer in self.stub.getEncoderIncrements(Proto.Empty()):
            widgetId = self.label2IdMap.widgetLabelToId(answer.objLabel)
            increments = answer.increments
            ret.append({'widgetId' : widgetId, 'increments' : increments})
        return ret

