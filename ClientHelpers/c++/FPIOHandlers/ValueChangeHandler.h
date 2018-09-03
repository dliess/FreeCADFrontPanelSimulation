#ifndef VALUE_CHANGE_HANDLER_H
#define VALUE_CHANGE_HANDLER_H

template<class CallbackContainer>
class ValueChangeHandler
{
public:
    ValueChangeHandler(CallbackContainer& callbacks) :
        m_rCallbacks(callbacks)
    {}
    template<class ValueHolder, class Widget>
    void operator()(ValueHolder&  valHolder,
                    const Widget& widget)
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
    CallbackContainer& m_rCallbacks;
};


#endif