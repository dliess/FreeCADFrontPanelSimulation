#ifndef FP_INPUT_HANDLER_H
#define FP_INPUT_HANDLER_H

#include "WidgetTypes.h"
#include "ValueContainer_Spec.h"
#include "CallbackContainer_Spec.h"
#include "ValueChangeHandler.h"
#include "Widget_Spec.h"
#include "CallbackIf_Spec.h"

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
        m_rotEncValues.forEach(ValueChangeHandler<EncCbContainer>(m_encCallbacks));
        m_btnValues.forEach(ValueChangeHandler<BtnCbContainer>(m_btnCallbacks));
        m_touchValues.forEach(ValueChangeHandler<TouchCbContainer>(m_touchCallbacks));
    }


    WidgetTypes::Potentiometer::ValueType potValue(const PotWidget& widget)
    {
        auto valHolder = m_potValues.get(widget);
        if(valHolder)
        {
            return valHolder->value();
        }
        return 0;
    }
    WidgetTypes::Button::ValueType btnValue(const BtnWidget& widget)
    {
        auto valHolder = m_btnValues.get(widget);
        if(valHolder)
        {
            return valHolder->value();
        }
        return WidgetTypes::Button::State::Released;
    }
    WidgetTypes::TouchSurface::ValueType touchValue(const TouchWidget& widget)
    {
        auto valHolder = m_touchValues.get(widget);
        if(valHolder)
        {
            return valHolder->value();
        }
        return {0,0};
    }

    void registerPotCb(PotCallback& cbIf, const PotWidget& widget)
    {
        m_potCallbacks.forWidget(widget, CbSetter<PotCallback>(cbIf));
    }
    void unregisterPotCb(PotCallback& cbIf, const PotWidget& widget)
    {
        m_potCallbacks.forWidget(widget, CbEraser<PotCallback>(cbIf));
    }
    void registerEncCb(EncCallback& cbIf, const EncWidget& widget)
    {
        m_encCallbacks.forWidget(widget, CbSetter<EncCallback>(cbIf));
    }
    void unregisterEncCb(EncCallback& cbIf, const EncWidget& widget)
    {
        m_encCallbacks.forWidget(widget, CbEraser<EncCallback>(cbIf));
    }
    void registerBtnCb(BtnCallback& cbIf, const BtnWidget& widget)
    {
        m_btnCallbacks.forWidget(widget, CbSetter<BtnCallback>(cbIf));
    }
    void unregisterBtnCb(BtnCallback& cbIf, const BtnWidget& widget)
    {
        m_btnCallbacks.forWidget(widget, CbEraser<BtnCallback>(cbIf));
    }
    void registerTouchCb(TouchCallback& cbIf, const TouchWidget& widget)
    {
        m_touchCallbacks.forWidget(widget, CbSetter<TouchCallback>(cbIf));
    }
    void unregisterTouchCb(TouchCallback& cbIf, const TouchWidget& widget)
    {
        m_touchCallbacks.forWidget(widget, CbEraser<TouchCallback>(cbIf));
    }

private:
    FpHal& m_rFpHal;

    PotValContainer   m_potValues;
    EncIncrContainer  m_rotEncValues;
    BtnValContainer   m_btnValues;
    TouchValContainer m_touchValues;

    PotCbContainer   m_potCallbacks;
    EncCbContainer   m_encCallbacks;
    BtnCbContainer   m_btnCallbacks;
    TouchCbContainer m_touchCallbacks;

    template<class CallbackIf>
    class CbSetter
    {
    public:
        CbSetter(CallbackIf& cbIf) :
           m_rCbIf(cbIf)
           {}
        template<class CbStack, class Widget>
        void operator()(CbStack&      cbStack,
                        const Widget& widget)
        {
            cbStack.pushBack(&m_rCbIf);
        }
    private:
        CallbackIf& m_rCbIf;
    };

    template<class CallbackIf>
    class CbEraser
    {
    public:
        CbEraser(CallbackIf& cbIf) :
           m_rCbIf(cbIf)
           {}
        template<class CbStack, class Widget>
        void operator()(CbStack&      cbStack,
                        const Widget& widget)
        {
            cbStack.remove(&m_rCbIf);
        }
    private:
        CallbackIf& m_rCbIf;
    };
};

#endif