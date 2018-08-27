#include <gtest/gtest.h>
#include "CallbackStack.h"

class ICallback
{
public:
    virtual void callback_fn() = 0;
};

class CBImpl : public ICallback
{
public:
    virtual void callback_fn(){};
};
 
TEST(CallbackStackTest, EmptyStack) {
    CallbackStack<ICallback, 1> cbStack1;
    CallbackStack<ICallback, 2> cbStack2;
    CallbackStack<ICallback, 3> cbStack3;
    ASSERT_EQ(nullptr, cbStack1.getActual());
    ASSERT_EQ(nullptr, cbStack2.getActual());
    ASSERT_EQ(nullptr, cbStack3.getActual());
}

TEST(CallbackStackTest, FillStack) {
    CallbackStack<ICallback, 1> cbStack1;
    CallbackStack<ICallback, 2> cbStack2;
    CallbackStack<ICallback, 3> cbStack3;
    CBImpl fun1;
    CBImpl fun2;
    CBImpl fun3;
    CBImpl fun4;

    cbStack1.pushBack(&fun1);
    ASSERT_EQ(&fun1, cbStack1.getActual());
    cbStack1.pushBack(&fun2);
    ASSERT_EQ(&fun2, cbStack1.getActual());
    cbStack1.pushBack(&fun3);
    ASSERT_EQ(&fun3, cbStack1.getActual());

    cbStack2.pushBack(&fun1);
    ASSERT_EQ(&fun1, cbStack2.getActual());
    cbStack2.pushBack(&fun2);
    ASSERT_EQ(&fun2, cbStack2.getActual());
    cbStack2.pushBack(&fun3);
    ASSERT_EQ(&fun3, cbStack2.getActual());

    cbStack3.pushBack(&fun1);
    ASSERT_EQ(&fun1, cbStack3.getActual());
    cbStack3.pushBack(&fun2);
    ASSERT_EQ(&fun2, cbStack3.getActual());
    cbStack3.pushBack(&fun3);
    ASSERT_EQ(&fun3, cbStack3.getActual());
    cbStack3.pushBack(&fun4);
    ASSERT_EQ(&fun4, cbStack3.getActual());
}

TEST(CallbackStackTest, ClearAll) {
    CallbackStack<ICallback, 1> cbStack1;
    CallbackStack<ICallback, 2> cbStack2;
    CallbackStack<ICallback, 3> cbStack3;
    CBImpl fun1;
    CBImpl fun2;
    CBImpl fun3;
    CBImpl fun4;

    cbStack1.pushBack(&fun1);
    cbStack1.remove(&fun2);
    ASSERT_EQ(&fun1, cbStack1.getActual());
    cbStack1.remove(&fun1);
    ASSERT_EQ(nullptr, cbStack1.getActual());

    cbStack2.pushBack(&fun1);
    cbStack2.pushBack(&fun1);
    cbStack2.remove(&fun2);
    ASSERT_EQ(&fun1, cbStack2.getActual());
    cbStack2.remove(&fun1);
    ASSERT_EQ(nullptr, cbStack2.getActual());

    cbStack3.pushBack(&fun1);
    cbStack3.pushBack(&fun1);
    cbStack3.pushBack(&fun1);
    cbStack3.remove(&fun2);
    ASSERT_EQ(&fun1, cbStack3.getActual());
    cbStack3.remove(&fun1);
    ASSERT_EQ(nullptr, cbStack3.getActual());
}

TEST(CallbackStackTest, ClearFromTop) {
    CallbackStack<ICallback, 2> cbStack2;
    CallbackStack<ICallback, 3> cbStack3;
    CBImpl fun1;
    CBImpl fun2;
    CBImpl fun3;
    CBImpl fun4;

    cbStack2.pushBack(&fun1);
    cbStack2.pushBack(&fun2);
    cbStack2.remove(&fun2);
    ASSERT_EQ(&fun1, cbStack2.getActual());
    cbStack2.remove(&fun1);
    ASSERT_EQ(nullptr, cbStack2.getActual());

    cbStack3.pushBack(&fun1);
    cbStack3.pushBack(&fun2);
    cbStack3.pushBack(&fun3);
    cbStack3.pushBack(&fun4);

    cbStack3.remove(&fun4);
    ASSERT_EQ(&fun3, cbStack3.getActual());
    cbStack3.remove(&fun3);
    ASSERT_EQ(&fun2, cbStack3.getActual());
    cbStack3.remove(&fun2);
    ASSERT_EQ(nullptr, cbStack3.getActual());
}

TEST(CallbackStackTest, ClearFromBottom) {
    CallbackStack<ICallback, 2> cbStack2;
    CallbackStack<ICallback, 3> cbStack3;
    CBImpl fun1;
    CBImpl fun2;
    CBImpl fun3;
    CBImpl fun4;

    cbStack2.pushBack(&fun1);
    cbStack2.pushBack(&fun2);
    cbStack2.remove(&fun1);
    ASSERT_EQ(&fun2, cbStack2.getActual());
    cbStack2.remove(&fun2);
    ASSERT_EQ(nullptr, cbStack2.getActual());

    cbStack3.pushBack(&fun1);
    cbStack3.pushBack(&fun2);
    cbStack3.pushBack(&fun3);
    cbStack3.pushBack(&fun4);

    cbStack3.remove(&fun1);
    ASSERT_EQ(&fun4, cbStack3.getActual());
    cbStack3.remove(&fun2);
    ASSERT_EQ(&fun4, cbStack3.getActual());
    cbStack3.remove(&fun3);
    ASSERT_EQ(&fun4, cbStack3.getActual());
    cbStack3.remove(&fun4);
    ASSERT_EQ(nullptr, cbStack3.getActual());
}