#include "GrpcClient.h"
#include <grpcpp/grpcpp.h>

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;


GrpcClient::GrpcClient(const std::string& serverAddress) :
    m_stub(FPSimulation::NewStub(grpc::CreateChannel(
      serverAddress, grpc::InsecureChannelCredentials())))
    {}

bool GrpcClient::led_setColor(const LedSetColorRequest &request)
{
    Empty reply;
    ClientContext context;
    Status status = m_stub->led_setColor(&context, request, &reply);
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}

bool GrpcClient::display_setPixels(const DisplaySetPixelsRequest &request)
{
    Empty reply;
    ClientContext context;
    Status status = m_stub->display_setPixels(&context, request, &reply);
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}

bool GrpcClient::display_setSubWindowPixels(const DisplaySubWindowPixelsRequest &request)
{
    Empty reply;
    ClientContext context;
    Status status = m_stub->display_setSubWindowPixels(&context, request, &reply);
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}

bool GrpcClient::display_drawRectangle(const DisplayDrawRectangleRequest &request)
{
    Empty reply;
    ClientContext context;
    Status status = m_stub->display_drawRectangle(&context, request, &reply);
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}

bool GrpcClient::display_drawLine(const DisplayDrawLineRequest &request)
{
    Empty reply;
    ClientContext context;
    Status status = m_stub->display_drawLine(&context, request, &reply);
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}

bool GrpcClient::display_setActiveFont(const DisplaySetActiveFontRequest &request)
{
    Empty reply;
    ClientContext context;
    Status status = m_stub->display_setActiveFont(&context, request, &reply);
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}

bool GrpcClient::display_drawText(const DisplayDrawTextRequest &request)
{
    Empty reply;
    ClientContext context;
    Status status = m_stub->display_drawText(&context, request, &reply);
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}

bool GrpcClient::display_getResolution( const DisplayResolutionRequest& request,
                                        DisplayResolutionAnswer& answer )
{
    ClientContext context;
    Status status = m_stub->display_getResolution(&context, request, &answer);
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}

bool GrpcClient::display_clearDisplay(const DisplayClearDisplayRequest &request)
{
    Empty reply;
    ClientContext context;
    Status status = m_stub->display_clearDisplay(&context, request, &reply);
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}
bool GrpcClient::getButtonStates(std::vector<GetButtonStateAnswer>& answer)
{
    return true;
}
bool GrpcClient::getEncoderIncrements(std::vector<GetEncoderIncrementsAnswer>& answer)
{
    return true;
}
bool GrpcClient::getPotentiometerValues(std::vector<GetPotentiometerValuesAnswer>& answer)
{
    return true;
}
bool GrpcClient::movePotentiometerToValue(const MovePotentiometerRequest &request)
{
    Empty reply;
    ClientContext context;
    Status status = m_stub->movePotentiometerToValue(&context, request, &reply);
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}
bool GrpcClient::getTouchValue(std::vector<GetTouchValueAnswer>& answer)
{
    return true;
}

