#ifndef TEST_CALLBACKS_H
#define TEST_CALLBACKS_H

#include "CallbackIf_Spec.h"
#include "Widget_Spec.h"

class TestBtnCB : public BtnCallback
{
public:
    TestBtnCB() : m_callCount(0){};
    void valueChangedCb(const BtnValue& value, const BtnWidget& widget) override
    {
        ++m_callCount;
    }
    uint32_t getCallCount() const {return m_callCount;}
    void clearCallCount() {m_callCount = 0;}
public:
    uint32_t m_callCount;
};

class TestPotCB : public PotCallback
{
public:
    TestPotCB() : m_sumValue(0){};
    void valueChangedCb(const PotValue& value, const PotWidget& widget) override
    {
        m_sumValue += value;
    }
    PotValue getSumValue() const {return m_sumValue;}
    void clearSumValue() {m_sumValue = 0;}
public:
    PotValue m_sumValue;
};

class TestEncCB : public EncCallback
{
public:
    TestEncCB() : m_sumValue(0){};
    void valueChangedCb(const EncValue& value, const EncWidget& widget) override
    {
        m_sumValue += value;
    }
    EncValue getSumValue() const {return m_sumValue;}
    void clearSumValue() {m_sumValue = 0;}
public:
    EncValue m_sumValue;
};

class TestTouchCB : public TouchCallback
{
public:
    TestTouchCB() : m_sumValue(){};
    void valueChangedCb(const TouchValue& value, const TouchWidget& widget) override
    {
        m_sumValue = m_sumValue + value;
    }
    TouchValue getSumValue() const {return m_sumValue;}
    void clearSumValue() {m_sumValue = 0;}
public:
    TouchValue m_sumValue;
};


#endif