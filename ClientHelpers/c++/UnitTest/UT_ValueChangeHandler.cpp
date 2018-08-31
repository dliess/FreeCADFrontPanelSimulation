#include <gtest/gtest.h>
#include "ValueChangeHandler.h"

class TestCallbackIf
{
public:
    TestCallbackIf() : m_val(0), m_widget(0), m_cbHasBeenCalled(false){}
    void valueChangedCb(int val, unsigned int widget){m_val = val; m_widget = widget; m_cbHasBeenCalled = true;}

    int getVal() const {return m_val;}
    unsigned int getWidget() const {return m_widget; }
    bool getIfCbHasBeenCalled() {if(m_cbHasBeenCalled) {m_cbHasBeenCalled = false; return true;} return false;}
private:
    int          m_val;
    unsigned int m_widget;
    bool m_cbHasBeenCalled;
};

class TestCBStack
{
public:
    TestCBStack(TestCallbackIf* cbIf) : m_pTestCbIf(cbIf) {}
    TestCallbackIf* getActual() {return m_pTestCbIf;};
private:
    TestCallbackIf* m_pTestCbIf;
};

class TestValueHolder
{
public:
    TestValueHolder() : m_val(0), m_hasChanged(false), m_resetCalled(false){}
    bool hasChanged() {return m_hasChanged;}
    const int& value() {return m_val;}
    void resetState() {m_resetCalled = true;}

    void setValue(int val) {m_val = val;}
    void setValueHasChanged(bool changed){ m_hasChanged = changed; }
    bool hasBeenReset() {return m_resetCalled;};
private:
    int  m_val;
    bool m_hasChanged;
    bool m_resetCalled;
};

class TestCallbackContainer
{
public:
    TestCallbackContainer(TestCBStack* cbs1, TestCBStack* cbs2, TestCBStack* cbs3) : 
        m_cbs{cbs1, cbs2, cbs3}
        {}
    TestCBStack* get(unsigned int widget){if(widget >= 3) return nullptr; return m_cbs[widget];};
private:
    TestCBStack* m_cbs[3];
};

class ValueChangeHandlerTest : public ::testing::Test {
 protected:
 ValueChangeHandlerTest() : 
    cbs1(&cbIf1),
    cbs2(&cbIf2),
    cbs3(&cbIf3),
    cbContainer(&cbs1, &cbs2, &cbs3),
    valueChangeHandler(cbContainer)
    {}

  // void SetUp() override {}
  // void TearDown() override {}

    TestCallbackIf cbIf1, cbIf2, cbIf3;
    TestCBStack    cbs1;
    TestCBStack    cbs2;
    TestCBStack    cbs3;
    TestCallbackContainer cbContainer;
    ValueChangeHandler<TestCallbackContainer> valueChangeHandler;

    TestValueHolder valHolder;
};

TEST_F(ValueChangeHandlerTest, TestValueHasChanged) {
    valHolder.setValue(5);
    valHolder.setValueHasChanged(true);

    valueChangeHandler(valHolder, 2);

    ASSERT_EQ(true, valHolder.hasBeenReset());

    ASSERT_EQ(false, cbIf1.getIfCbHasBeenCalled());
    ASSERT_EQ(0, cbIf1.getVal());
    ASSERT_EQ(0, cbIf1.getWidget());

    ASSERT_EQ(false, cbIf2.getIfCbHasBeenCalled());
    ASSERT_EQ(0, cbIf2.getVal());
    ASSERT_EQ(0, cbIf2.getWidget());

    ASSERT_EQ(true, cbIf3.getIfCbHasBeenCalled());
    ASSERT_EQ(5, cbIf3.getVal());
    ASSERT_EQ(2, cbIf3.getWidget());
}

TEST_F(ValueChangeHandlerTest, TestValueHasNotChanged) {
    valHolder.setValue(5);
    valHolder.setValueHasChanged(false);

    valueChangeHandler(valHolder, 2);

    ASSERT_EQ(false, valHolder.hasBeenReset());

    ASSERT_EQ(false, cbIf1.getIfCbHasBeenCalled());
    ASSERT_EQ(0, cbIf1.getVal());
    ASSERT_EQ(0, cbIf1.getWidget());

    ASSERT_EQ(false, cbIf2.getIfCbHasBeenCalled());
    ASSERT_EQ(0, cbIf2.getVal());
    ASSERT_EQ(0, cbIf2.getWidget());

    ASSERT_EQ(false, cbIf3.getIfCbHasBeenCalled());
    ASSERT_EQ(0, cbIf3.getVal());
    ASSERT_EQ(0, cbIf3.getWidget());
}