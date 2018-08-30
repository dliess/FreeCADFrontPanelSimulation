#ifndef FP_INPUT_HANDLER_H
#define FP_INPUT_HANDLER_H

#include "WidgetTypes.h"
#include "ValueContainer.h"
#include "CallbackContainer.h"
#include "ValueChangeHandler.h"

template<class FpHal>
class FpInputHandler
{
public:
    FpInputHandler(FpHal& rFpHal) :
        m_rFpHal(rFpHal)
        {}
    void poll()
    {
        m_rFpHal.actualize(m_potValues);
        m_rFpHal.actualize(m_rotEncValues);
        m_rFpHal.actualize(m_btnValues);
        m_rFpHal.actualize(m_touchValues);

        m_potValues.forEach(ValueChangeHandler<WidgetTypes::Potentiometer>(m_potCallbacks));
        m_rotEncValues.forEach(ValueChangeHandler<WidgetTypes::Encoder>(m_rotEncCallbacks));
        m_btnValues.forEach(ValueChangeHandler<WidgetTypes::Button>(m_btnCallbacks));
        m_touchCallbacks.forEach(ValueChangeHandler<WidgetTypes::TouchSurface>(m_touchCallbacks));
    }

private:
    FpHal& m_rFpHal;

    ValueContainer<WidgetTypes::Potentiometer> m_potValues;
    ValueContainer<WidgetTypes::Encoder>       m_rotEncValues;
    ValueContainer<WidgetTypes::Button>        m_btnValues;
    ValueContainer<WidgetTypes::TouchSurface>  m_touchValues;

    CallbackContainer<WidgetTypes::Potentiometer> m_potCallbacks;
    CallbackContainer<WidgetTypes::Encoder>       m_rotEncCallbacks;
    CallbackContainer<WidgetTypes::Button>        m_btnCallbacks;
    CallbackContainer<WidgetTypes::TouchSurface>  m_touchCallbacks;
};

#endif