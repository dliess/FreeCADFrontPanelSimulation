#include "WidgetTopology_Spec.h"
#include "Widget_Spec.h"
#include "CallbackContainer_Spec.h"
#include "Vector2D.h"
#include <gtest/gtest.h>
#include "FpInputHandler.h" //important to include it after topology classes
#include "TestFpHal.h"
#include "TestCallbacks.h"

TEST(FpInputHandlerTest, ButtonCbTest) {
    TestFpHal hal;
    FpInputHandler<TestFpHal> fpInputHandler(hal);
    TestBtnCB btnCb;
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

TEST(FpInputHandlerTest, PotentiometerCbTest) {
    TestFpHal hal;
    FpInputHandler<TestFpHal> fpInputHandler(hal);
    TestPotCB potCb1;
    TestPotCB potCb2;
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

TEST(FpInputHandlerTest, EncoderCbTest) {
    TestFpHal hal;
    FpInputHandler<TestFpHal> fpInputHandler(hal);
    TestEncCB encCb1;
    TestEncCB encCb2;
    fpInputHandler.registerEncCb(encCb1, EncWidget(EncId::EncMatrix, Vec2D(Vec2D::ALL, Vec2D::ALL)));
    fpInputHandler.registerEncCb(encCb2, EncWidget(EncId::EncMatrix, Vec2D(1,1)));

    *hal.encIncrements.get(EncWidget(EncId::EncMatrix, Vec2D(1,4))) = 10;
    fpInputHandler.poll();
    ASSERT_EQ(10, encCb1.getSumValue());

    encCb1.clearSumValue();
    encCb2.clearSumValue();
    fpInputHandler.poll();
    ASSERT_EQ(10, encCb1.getSumValue());

    encCb1.clearSumValue();
    encCb2.clearSumValue();
    *hal.encIncrements.get(EncWidget(EncId::EncMatrix, Vec2D(1,4))) = 0;
    *hal.encIncrements.get(EncWidget(EncId::EncMatrix, Vec2D(1,0))) = 10;
    *hal.encIncrements.get(EncWidget(EncId::EncMatrix, Vec2D(1,1))) = 20;
    *hal.encIncrements.get(EncWidget(EncId::EncMatrix, Vec2D(1,6))) = 30;
    fpInputHandler.poll();
    ASSERT_EQ(40, encCb1.getSumValue());
    ASSERT_EQ(20, encCb2.getSumValue());

    fpInputHandler.unregisterEncCb(encCb2, EncWidget(EncId::EncMatrix, Vec2D(1,1)));
    encCb1.clearSumValue();
    encCb2.clearSumValue();
    *hal.encIncrements.get(EncWidget(EncId::EncMatrix, Vec2D(1,0))) = 30;
    *hal.encIncrements.get(EncWidget(EncId::EncMatrix, Vec2D(1,1))) = 40;
    *hal.encIncrements.get(EncWidget(EncId::EncMatrix, Vec2D(1,6))) = 50;
    fpInputHandler.poll();
    ASSERT_EQ(120, encCb1.getSumValue());
    ASSERT_EQ(0,  encCb2.getSumValue());
}

TEST(FpInputHandlerTest, TouchCbTest) {
    TestFpHal hal;
    FpInputHandler<TestFpHal> fpInputHandler(hal);
    TestTouchCB touchCb;
    fpInputHandler.registerTouchCb(touchCb, TouchWidget(TouchId::Touch1, Vec2D(Vec2D::ALL, Vec2D::ALL)));
    fpInputHandler.registerTouchCb(touchCb, TouchWidget(TouchId::Touch2, Vec2D(Vec2D::ALL, Vec2D::ALL)));
    fpInputHandler.registerTouchCb(touchCb, TouchWidget(TouchId::Touch3, Vec2D(Vec2D::ALL, Vec2D::ALL)));

    *hal.touchValues.get(TouchWidget(TouchId::Touch1, Vec2D(0,0))) = {10 ,5};
    *hal.touchValues.get(TouchWidget(TouchId::Touch3, Vec2D(0,0))) = {10, 5};
    fpInputHandler.poll();
    ASSERT_EQ(TouchValue(20, 10), touchCb.getSumValue());

    touchCb.clearSumValue();
    fpInputHandler.poll();
    ASSERT_EQ(TouchValue(0, 0), touchCb.getSumValue());
}

TEST(FpInputHandlerTest, PotentiometerValGetTest) {
    TestFpHal hal;
    FpInputHandler<TestFpHal> fpInputHandler(hal);
    hal.potValues.forEach([](PotValue &data, const PotWidget &widget){data = 11;});
    ASSERT_EQ(0, fpInputHandler.potValue(PotWidget(PotId::PotMatrix, Vec2D(0,0))));
    fpInputHandler.poll();
    ASSERT_EQ(11, fpInputHandler.potValue(PotWidget(PotId::PotMatrix, Vec2D(0,0))));
    ASSERT_EQ(0, fpInputHandler.potValue(PotWidget(PotId::PotMatrix, Vec2D(100,100))));
}
TEST(FpInputHandlerTest, ButtonStateGetTest) {
    TestFpHal hal;
    FpInputHandler<TestFpHal> fpInputHandler(hal);
    hal.btnValues.forEach([](BtnValue &data, const BtnWidget &widget){data = WidgetTypes::Button::State::Pressed;});
    ASSERT_EQ(WidgetTypes::Button::State::Released, fpInputHandler.btnValue(BtnWidget(BtnId::Menu, Vec2D(0,0))));
    fpInputHandler.poll();
    ASSERT_EQ(WidgetTypes::Button::State::Pressed, fpInputHandler.btnValue(BtnWidget(BtnId::Menu, Vec2D(0,0))));
    ASSERT_EQ(WidgetTypes::Button::State::Released, fpInputHandler.btnValue(BtnWidget(BtnId::Menu, Vec2D(100,100))));
}
TEST(FpInputHandlerTest, TouchValueGetTest) {
    TestFpHal hal;
    FpInputHandler<TestFpHal> fpInputHandler(hal);
    hal.touchValues.forEach([](TouchValue &data, const TouchWidget &widget){data = TouchValue(11,22);});
    ASSERT_EQ(TouchValue(0,0), fpInputHandler.touchValue(TouchWidget(TouchId::Touch1, Vec2D(0,0))));
    fpInputHandler.poll();
    ASSERT_EQ(TouchValue(11,22), fpInputHandler.touchValue(TouchWidget(TouchId::Touch1, Vec2D(0,0))));
    ASSERT_EQ(TouchValue(0,0), fpInputHandler.touchValue(TouchWidget(TouchId::Touch1, Vec2D(100,100))));
}
