#ifndef GRPC_CLIENT_H
#define GRPC_CLIENT_H

#include <memory> // shared_ptr
#include <grpcpp/grpcpp.h>

using grpc::Channel;
 

class GrpcClient
{
public:
    GrpcClient(std::shared_ptr<Channel> channel);

private:
      std::unique_ptr<Greeter::Stub> m_stub;
};

#endif