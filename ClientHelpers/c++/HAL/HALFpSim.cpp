#ifndef FP_HAL_SIM_H
#define FP_HAL_SIM_H

#include "WidgetTypes.h"
#include "ValueContainer.h"

class FpHalSim
{
public:
    void update(ValueContainer<WidgetTypes::Potentiometer>& container);
    void update(ValueContainer<WidgetTypes::Encoder>& container);
    void update(ValueContainer<WidgetTypes::Button>& container);
    void update(ValueContainer<WidgetTypes::TouchSurface>& container);
};

#endif