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
        m_rFpHal.update(m_potValues);
        m_rFpHal.update(m_rotEncValues);
        m_rFpHal.update(m_btnValues);
        m_rFpHal.update(m_touchValues);

        m_potValues.forEach(ValueChangeHandler<PotCbContainer>(m_potCallbacks));
        m_rotEncValues.forEach(ValueChangeHandler<EncCbContainer>(m_rotEncCallbacks));
        m_btnValues.forEach(ValueChangeHandler<BtnCbContainer>(m_btnCallbacks));
        m_touchValues.forEach(ValueChangeHandler<TouchCbContainer>(m_touchCallbacks));
    }

private:
    FpHal& m_rFpHal;

    PotValContainer   m_potValues;
    EncIncrContainer  m_rotEncValues;
    BtnValContainer   m_btnValues;
    TouchValContainer m_touchValues;

    PotCbContainer   m_potCallbacks;
    EncCbContainer   m_rotEncCallbacks;
    BtnCbContainer   m_btnCallbacks;
    TouchCbContainer m_touchCallbacks;
};

#endif