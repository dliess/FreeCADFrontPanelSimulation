#include <gtest/gtest.h>
#include "IncrementHolder.h"


TEST(IncrementHolderTest, State) {
    IncrementHolder<int> incrementHolder;
    ASSERT_EQ(false, incrementHolder.hasChanged());
    incrementHolder.resetState();
    ASSERT_EQ(false, incrementHolder.hasChanged());
    incrementHolder.set(4);
    ASSERT_EQ(true, incrementHolder.hasChanged());
}

TEST(IncrementHolderTest, Value) {
    IncrementHolder<int> incrementHolder;
    ASSERT_EQ(0, incrementHolder.value());
    incrementHolder.set(4);
    ASSERT_EQ(4, incrementHolder.value());
}


