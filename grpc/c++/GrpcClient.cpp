#include "GrpcClient.h"

GrpcClient::GrpcClient(std::shared_ptr<Channel> channel) :
    m_stub(Greeter::NewStub(channel))
    {}
