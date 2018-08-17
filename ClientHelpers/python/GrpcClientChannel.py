import grpc

class GrpcClientChannel():
    def __init__(self, addr):
        channel = grpc.insecure_channel(addr)
        self.stub = GRPC.FPSimulationStub(channel)
