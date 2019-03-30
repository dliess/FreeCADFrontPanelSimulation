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

bool GrpcClient::display_setPixels_ARGB32(const DisplaySetPixelsRequest_ARGB32 &request,
                                   Duration        &answer)
{
    ClientContext context;
    Status status = m_stub->display_setPixels_ARGB32(&context, request, &answer);
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}

bool GrpcClient::display_setSubWindowPixels_ARGB32(const DisplaySubWindowPixelsRequest_ARGB32 &request,
                                            Duration        &answer)
{
    ClientContext context;
    Status status = m_stub->display_setSubWindowPixels_ARGB32(&context, request, &answer);
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

bool GrpcClient::display_getTextSize( const DisplayGetTextSizeRequest &request,
                                      DisplayGetTextSizeAnswer& answer)
{
    ClientContext context;
    Status status = m_stub->display_getTextSize(&context, request, &answer);
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
    Empty request;
    ClientContext context;
    auto reader = m_stub->getButtonStates(&context, request);
    GetButtonStateAnswer oneAnswer;
    while(reader->Read(&oneAnswer))
    {
        answer.push_back(oneAnswer);
    }
    Status status = reader->Finish();
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}

bool GrpcClient::getButton3dStates(std::vector<GetButton3dStateAnswer>& answer)
{
    Empty request;
    ClientContext context;
    auto reader = m_stub->getButton3dStates(&context, request);
    GetButton3dStateAnswer oneAnswer;
    while(reader->Read(&oneAnswer))
    {
        answer.push_back(oneAnswer);
    }
    Status status = reader->Finish();
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}

bool GrpcClient::getButton5dStates(std::vector<GetButton5dStateAnswer>& answer)
{
    Empty request;
    ClientContext context;
    auto reader = m_stub->getButton5dStates(&context, request);
    GetButton5dStateAnswer oneAnswer;
    while(reader->Read(&oneAnswer))
    {
        answer.push_back(oneAnswer);
    }
    Status status = reader->Finish();
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}

bool GrpcClient::getEncoderIncrements(std::vector<GetEncoderIncrementsAnswer>& answer)
{
    Empty request;
    ClientContext context;
    auto reader = m_stub->getEncoderIncrements(&context, request);
    GetEncoderIncrementsAnswer oneAnswer;
    while(reader->Read(&oneAnswer))
    {
        answer.push_back(oneAnswer);
    }
    Status status = reader->Finish();
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}
bool GrpcClient::getPotentiometerValues(std::vector<GetPotentiometerValuesAnswer>& answer)
{
    Empty request;
    ClientContext context;
    auto reader = m_stub->getPotentiometerValues(&context, request);
    GetPotentiometerValuesAnswer oneAnswer;
    while(reader->Read(&oneAnswer))
    {
        answer.push_back(oneAnswer);
    }
    Status status = reader->Finish();
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
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
    Empty request;
    ClientContext context;
    auto reader = m_stub->getTouchValue(&context, request);
    GetTouchValueAnswer oneAnswer;
    while(reader->Read(&oneAnswer))
    {
        answer.push_back(oneAnswer);
    }
    Status status = reader->Finish();
    if (status.ok()) {
      return true;
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return false;
    }
}

