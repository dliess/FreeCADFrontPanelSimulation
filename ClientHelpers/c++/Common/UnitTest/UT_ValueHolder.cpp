#include <gtest/gtest.h>
#include "ValueHolder.h"


TEST(ValueHolderTest, State) {
    ValueHolder<int> incrementHolder;
    ASSERT_EQ(false, incrementHolder.hasChanged());
    incrementHolder.resetState();
    ASSERT_EQ(false, incrementHolder.hasChanged());
    incrementHolder.set(4);
    ASSERT_EQ(true, incrementHolder.hasChanged());
}

TEST(ValueHolderTest, Value) {
    ValueHolder<int> incrementHolder;
    ASSERT_EQ(0, incrementHolder.value());
    incrementHolder.set(4);
    ASSERT_EQ(4, incrementHolder.value());
}


