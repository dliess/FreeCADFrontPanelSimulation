#ifndef FP_HAL_H
#define FP_HAL_H

#include "WidgetTypes.h"
#include "ValueContainer.h"

class FpHal
{
public:
    void update(ValueContainer<WidgetTypes::Potentiometer>& container);
    void update(ValueContainer<WidgetTypes::Encoder>& container);
    void update(ValueContainer<WidgetTypes::Button>& container);
    void update(ValueContainer<WidgetTypes::TouchSurface>& container);
};

#endif