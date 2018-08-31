#ifndef CALLBACK_IF_H
#define CALLBACK_IF_H

#include "Widget.h"
#include "WidgetTopology.h"

template<class WidgetType>
class CallbackIf
{
public:
    virtual void valueChangedCb(const typename WidgetType::ValueType& value, const Widget< WidgetTopology<WidgetType> >& widget) = 0;
};

#endif