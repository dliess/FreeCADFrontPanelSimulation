#ifndef VALUE_CHANGE_HANDLER_H
#define VALUE_CHANGE_HANDLER_H

#include "CallbackContainer.h"
#include "CallbackIf.h"
#include "WidgetTopology.h"
#include "Widget.h"

template<class WidgetType>
class ValueChangeHandler
{
public:
    ValueChangeHandler(CallbackContainer<WidgetType>& callbacks) :
        m_rCallbacks(callbacks)
    {}
    void operator()(typename WidgetType::ValueHolder&           valHolder,
                    const Widget< WidgetTopology<WidgetType> >& widget)
    {
        if(valHolder.hasChanged())
        {
            auto cbIf = m_rCallbacks.get(widget)->getActual();
            if(cbIf)
            {
                cbIf->valueChangedCb(valHolder.value(), widget);
            }
            valHolder.resetState();
        }
    }
private:
    CallbackContainer<WidgetType>& m_rCallbacks;
};

#endif