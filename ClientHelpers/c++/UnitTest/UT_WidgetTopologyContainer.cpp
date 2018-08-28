#include <gtest/gtest.h>
#include "WidgetTopologyContainer.h"

struct TopologyDim{uint8_t x; uint8_t y;};
class EmptyWidgetFunction
{
public:
    enum WidgetId{
        Last    = -1
    };
   static const TopologyDim& getDim(WidgetId widgetId)
   {
      static const TopologyDim dim = {0,0};
      return dim;
   }
};
class WidgetFunction
{
public:
    enum WidgetId{
        Widget1 = 0,
        Widget2 = 1,
        Widget3 = 2,
        Last    = Widget3
    };
   static const TopologyDim& getDim(WidgetId widgetId)
   {
      static const TopologyDim dim[WidgetId::Last + 1] = { {1, 1}, {1, 2}, {2, 2}};
      return dim[widgetId];
   }
};

TEST(WidgetTopologyContainerTest, GetTest) {
    WidgetTopologyContainer<int, WidgetFunction> container;
    ASSERT_NE(nullptr, container.get(WidgetFunction::WidgetId::Widget1, 0, 0));
    ASSERT_EQ(nullptr, container.get(WidgetFunction::WidgetId::Widget1, 1, 0));
    ASSERT_EQ(nullptr, container.get(WidgetFunction::WidgetId::Widget1, 0, 1));

    ASSERT_NE(nullptr, container.get(WidgetFunction::WidgetId::Widget2, 0, 0));
    ASSERT_NE(nullptr, container.get(WidgetFunction::WidgetId::Widget2, 0, 1));
    ASSERT_EQ(nullptr, container.get(WidgetFunction::WidgetId::Widget2, 1, 0));
    ASSERT_EQ(nullptr, container.get(WidgetFunction::WidgetId::Widget2, 0, 2));

    ASSERT_NE(nullptr, container.get(WidgetFunction::WidgetId::Widget3, 0, 0));
    ASSERT_NE(nullptr, container.get(WidgetFunction::WidgetId::Widget3, 1, 0));
    ASSERT_NE(nullptr, container.get(WidgetFunction::WidgetId::Widget3, 0, 1));
    ASSERT_NE(nullptr, container.get(WidgetFunction::WidgetId::Widget3, 1, 1));
    ASSERT_EQ(nullptr, container.get(WidgetFunction::WidgetId::Widget3, 0, 2));
    ASSERT_EQ(nullptr, container.get(WidgetFunction::WidgetId::Widget3, 2, 0));

    ASSERT_EQ(0, *container.get(WidgetFunction::WidgetId::Widget1, 0, 0));
    *container.get(WidgetFunction::WidgetId::Widget1, 0, 0) = 10;
    ASSERT_EQ(10, *container.get(WidgetFunction::WidgetId::Widget1, 0, 0));
}

TEST(WidgetTopologyContainerTest, EmptyTest) {
    WidgetTopologyContainer<int, EmptyWidgetFunction> emptyContainer;
    ASSERT_EQ(0, sizeof(emptyContainer));
    ASSERT_EQ(nullptr, emptyContainer.get(EmptyWidgetFunction::WidgetId::Last, 0, 0));
}