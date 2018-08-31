#include "WidgetTopology.h"
#include "WidgetTypes.h"

template<>
class WidgetTopology<WidgetTypes::Potentiometer>
{
public:
    enum WidgetId{
        Pot1       =  0,
        PotMatrix  =  1,
        Last       =  PotMatrix
    };
    static const Vec2D& getDim(WidgetId widgetId)
    {
        static const Vec2D dim[WidgetId::Last + 1] = {{1,1},{2,8}};
        return dim[widgetId];
    }
};

template<>
class WidgetTopology<WidgetTypes::Encoder>
{
public:
    enum WidgetId{
        EncMatrix = 0,
        Last      = EncMatrix
    };
    static const Vec2D& getDim(WidgetId widgetId)
    {
        static const Vec2D dim[WidgetId::Last + 1] = {{4,8}};
        return dim[widgetId];
    }
};

template<>
class WidgetTopology<WidgetTypes::Button>
{
public:
    enum WidgetId{
        Menu  = 0,
        Notes = 1,
        Last  = Notes
    };
    static const Vec2D& getDim(WidgetId widgetId)
    {
        static const Vec2D dim[WidgetId::Last + 1] = {{1,1},{1,24}};
        return dim[widgetId];
    }
};

template<>
class WidgetTopology<WidgetTypes::TouchSurface>
{
public:
    enum WidgetId{
        Touch1  =  0,
        Touch2  =  1,
        Touch3  =  2,
        Last    =  Touch3
    };
    static const Vec2D& getDim(WidgetId widgetId)
    {
        static const Vec2D dim[WidgetId::Last + 1] = {{1,1},{1,1},{1,1}};
        return dim[widgetId];
    }
};

#include <gtest/gtest.h>
#include "FpInputHandler.h" //important to include it after topology classes

class TestFpHal
{
public:
    void update(PotValContainer& container)
    {
        potValues.forEach(ValueMover<PotValContainer>(container));
    }
    void update(EncIncrContainer& container)
    {
        encIncrements.forEach(ValueMover<EncIncrContainer>(container));
    }
    void update(BtnValContainer& container)
    {
        btnValues.forEach(ValueMover<BtnValContainer>(container));
    }
    void update(TouchValContainer& container)
    {
        touchValues.forEach(ValueMover<TouchValContainer>(container));
    }

    
    template<class WidgetType>
    using Container = WidgetTopologyContainer< typename WidgetType::ValueType, WidgetTopology<WidgetType> >;
    Container<WidgetTypes::Potentiometer> potValues;
    Container<WidgetTypes::Encoder>       encIncrements;
    Container<WidgetTypes::Button>        btnValues;
    Container<WidgetTypes::TouchSurface>  touchValues;

private:
    template<class DestContainer>
    class ValueMover
    {
    public:
        ValueMover(DestContainer& destContainer) : 
            m_rDestContainer(destContainer)
            {}
        template<class ValueType, class Widget>
        void operator()(ValueType& val, const Widget& widget)
        {
            m_rDestContainer.get(widget)->set(val);
            reset<ValueType>(val);
        } 
    private:
        DestContainer& m_rDestContainer;
    };

};


TEST(FpInputHandlerTest, Run) {
    TestFpHal hal;
    FpInputHandler<TestFpHal> fpInputHandler(hal);
    fpInputHandler.poll();
}