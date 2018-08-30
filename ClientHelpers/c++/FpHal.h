#ifndef FP_HAL_H
#define FP_HAL_H

#include "WidgetTypes.h"
#include "ValueContainer.h"

class FpHal
{
public:
    void actualize(ValueContainer<WidgetTypes::Potentiometer>& container);
    void actualize(ValueContainer<WidgetTypes::Encoder>& container);
    void actualize(ValueContainer<WidgetTypes::Button>& container);
    void actualize(ValueContainer<WidgetTypes::TouchSurface>& container);
};

#endif