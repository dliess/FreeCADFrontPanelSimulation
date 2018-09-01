#include "WidgetTopology.h"
#include "WidgetTypes.h"
#include "Vector2D.h"

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

using PotValue   = WidgetTypes::Potentiometer::ValueType;
using EncValue   = WidgetTypes::Encoder::ValueType;
using BtnValue   = WidgetTypes::Button::ValueType;
using TouchValue = WidgetTypes::TouchSurface::ValueType;

using PotId = WidgetTopology<WidgetTypes::Potentiometer>::WidgetId;
using EncId = WidgetTopology<WidgetTypes::Encoder>::WidgetId;
using BtnId = WidgetTopology<WidgetTypes::Button>::WidgetId;
using TouchId = WidgetTopology<WidgetTypes::TouchSurface>::WidgetId;


class BtnCB : public BtnCallback
{
public:
    BtnCB() : m_callCount(0){};
    void valueChangedCb(const BtnValue& value, const BtnWidget& widget) override
    {
        ++m_callCount;
    }
    uint32_t getCallCount() const {return m_callCount;}
    void clearCallCount() {m_callCount = 0;}
public:
    uint32_t m_callCount;
};

TEST(FpInputHandlerTest, ButtonTest) {
    TestFpHal hal;
    FpInputHandler<TestFpHal> fpInputHandler(hal);
    BtnCB btnCb;
    fpInputHandler.registerBtnCb(btnCb, BtnWidget(BtnId::Menu, Vec2D(Vec2D::ALL, Vec2D::ALL)));
    fpInputHandler.registerBtnCb(btnCb, BtnWidget(BtnId::Notes, Vec2D(Vec2D::ALL, Vec2D::ALL)));

    hal.btnValues.forEach([](BtnValue &data, const BtnWidget &widget){data = WidgetTypes::Button::State::Pressed;});
    fpInputHandler.poll();
    ASSERT_EQ(25, btnCb.getCallCount());

    btnCb.clearCallCount();
    hal.btnValues.forEach([](BtnValue &data, const BtnWidget &widget){data = WidgetTypes::Button::State::Pressed;});
    fpInputHandler.poll();
    ASSERT_EQ(0, btnCb.getCallCount());

    btnCb.clearCallCount();
    hal.btnValues.forEach([](BtnValue &data, const BtnWidget &widget){data = WidgetTypes::Button::State::Released;});
    fpInputHandler.poll();
    ASSERT_EQ(25, btnCb.getCallCount());
}

class PotCB : public PotCallback
{
public:
    PotCB() : m_sumValue(0){};
    void valueChangedCb(const PotValue& value, const PotWidget& widget) override
    {
        m_sumValue += value;
    }
    PotValue getSumValue() const {return m_sumValue;}
    void clearSumValue() {m_sumValue = 0;}
public:
    PotValue m_sumValue;
};

TEST(FpInputHandlerTest, PotentiometerTest) {
    TestFpHal hal;
    FpInputHandler<TestFpHal> fpInputHandler(hal);
    PotCB potCb1;
    PotCB potCb2;
    fpInputHandler.registerPotCb(potCb1, PotWidget(PotId::Pot1, Vec2D(Vec2D::ALL, Vec2D::ALL)));
    fpInputHandler.registerPotCb(potCb1, PotWidget(PotId::PotMatrix, Vec2D(Vec2D::ALL, Vec2D::ALL)));
    fpInputHandler.registerPotCb(potCb2, PotWidget(PotId::PotMatrix, Vec2D(1,1)));

    *hal.potValues.get(PotWidget(PotId::PotMatrix, Vec2D(1,4))) = 10;
    fpInputHandler.poll();
    ASSERT_EQ(10, potCb1.getSumValue());

    potCb1.clearSumValue();
    potCb2.clearSumValue();
    *hal.potValues.get(PotWidget(PotId::PotMatrix, Vec2D(1,0))) = 10;
    *hal.potValues.get(PotWidget(PotId::PotMatrix, Vec2D(1,1))) = 20;
    *hal.potValues.get(PotWidget(PotId::PotMatrix, Vec2D(1,6))) = 30;
    fpInputHandler.poll();
    ASSERT_EQ(40, potCb1.getSumValue());
    ASSERT_EQ(20, potCb2.getSumValue());

    fpInputHandler.unregisterPotCb(potCb2, PotWidget(PotId::PotMatrix, Vec2D(1,1)));
    potCb1.clearSumValue();
    potCb2.clearSumValue();
    *hal.potValues.get(PotWidget(PotId::PotMatrix, Vec2D(1,0))) = 30;
    *hal.potValues.get(PotWidget(PotId::PotMatrix, Vec2D(1,1))) = 40;
    *hal.potValues.get(PotWidget(PotId::PotMatrix, Vec2D(1,6))) = 50;
    fpInputHandler.poll();
    ASSERT_EQ(120, potCb1.getSumValue());
    ASSERT_EQ(0,  potCb2.getSumValue());
}
