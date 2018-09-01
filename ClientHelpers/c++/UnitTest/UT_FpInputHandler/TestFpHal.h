#ifndef TEST_FP_HAL_H
#define TEST_FP_HAL_H

#include "ValueContainer_Spec.h"

class TestFpHal
{
public:
    void update(PotValContainer& container)
    {
        potValues.forEach(ValueCopyer<PotValContainer>(container));
    }
    void update(EncIncrContainer& container)
    {
        encIncrements.forEach(ValueCopyer<EncIncrContainer>(container));
    }
    void update(BtnValContainer& container)
    {
        btnValues.forEach(ValueCopyer<BtnValContainer>(container));
    }
    void update(TouchValContainer& container)
    {
        touchValues.forEach(ValueCopyer<TouchValContainer>(container));
    }

    template<class WidgetType>
    using ValueContainer = WidgetTopologyContainer< typename WidgetType::ValueType, WidgetTopology<WidgetType> >;

    ValueContainer<WidgetTypes::Potentiometer> potValues;
    ValueContainer<WidgetTypes::Encoder>       encIncrements;
    ValueContainer<WidgetTypes::Button>        btnValues;
    ValueContainer<WidgetTypes::TouchSurface>  touchValues;

private:
    template<class DestContainer>
    class ValueCopyer
    {
    public:
        ValueCopyer(DestContainer& destContainer) : 
            m_rDestContainer(destContainer)
            {}
        template<class ValueType, class Widget>
        void operator()(ValueType& val, const Widget& widget)
        {
            m_rDestContainer.get(widget)->set(val);
        } 
    private:
        DestContainer& m_rDestContainer;
    };
};


#endif