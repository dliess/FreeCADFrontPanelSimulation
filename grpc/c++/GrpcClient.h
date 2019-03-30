#ifndef GRPC_CLIENT_H
#define GRPC_CLIENT_H

#include <memory> // shared_ptr
#include <vector>
#include "FPSimulation.pb.h"
#include "FPSimulation.grpc.pb.h"
 

class GrpcClient
{
public:
    GrpcClient(const std::string& serverAddress);
    bool led_setColor(const LedSetColorRequest &request);
    bool display_setPixels_ARGB32(const DisplaySetPixelsRequest_ARGB32 &request, Duration& answer);
    bool display_setSubWindowPixels_ARGB32(const DisplaySubWindowPixelsRequest_ARGB32 &request, Duration& answer);
    bool display_drawRectangle(const DisplayDrawRectangleRequest &request);
    bool display_drawLine(const DisplayDrawLineRequest &request);
    bool display_setActiveFont(const DisplaySetActiveFontRequest &request);
    bool display_drawText(const DisplayDrawTextRequest &request);
    bool display_getResolution(const DisplayResolutionRequest& request, DisplayResolutionAnswer& answer);
    bool display_clearDisplay(const DisplayClearDisplayRequest &request);
    bool display_getTextSize(const DisplayGetTextSizeRequest &request, DisplayGetTextSizeAnswer& answer);
    bool getButtonStates(std::vector<GetButtonStateAnswer>& answer);
    bool getButton3dStates(std::vector<GetButton3dStateAnswer>& answer);
    bool getButton5dStates(std::vector<GetButton5dStateAnswer>& answer);
    bool getEncoderIncrements(std::vector<GetEncoderIncrementsAnswer>& answer);
    bool getPotentiometerValues(std::vector<GetPotentiometerValuesAnswer>& answer);
    bool movePotentiometerToValue(const MovePotentiometerRequest &request);
    bool getTouchValue(std::vector<GetTouchValueAnswer>& answer);

private:
    std::unique_ptr<FPSimulation::Stub> m_stub;
};

#endif