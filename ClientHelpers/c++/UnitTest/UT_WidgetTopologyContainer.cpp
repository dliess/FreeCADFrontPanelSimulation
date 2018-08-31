#include <gtest/gtest.h>
#include "WidgetTopologyContainer.h"
#include "Vector2D.h"

class TestEmptyWidgetTopology
{
public:
    enum WidgetId{
        Last    = -1
    };
   static const Vec2D& getDim(WidgetId widgetId)
   {
      static const Vec2D dim = {0,0};
      return dim;
   }
};
class TestWidgetTopology
{
public:
    enum WidgetId{
        Widget1 = 0,
        Widget2 = 1,
        Widget3 = 2,
        Last    = Widget3
    };
   static const Vec2D& getDim(WidgetId widgetId)
   {
      static const Vec2D dim[WidgetId::Last + 1] = { {1, 1}, {1, 2}, {2, 2} };
      return dim[widgetId];
   }
};

TEST(WidgetTopologyContainerTest, GetTest) {
    WidgetTopologyContainer<int, TestWidgetTopology> container;
    ASSERT_NE(nullptr, container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget1, Vec2D(0, 0))));
    ASSERT_EQ(nullptr, container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget1, Vec2D(1, 0))));
    ASSERT_EQ(nullptr, container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget1, Vec2D(0, 1))));

    ASSERT_NE(nullptr, container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 0))));
    ASSERT_NE(nullptr, container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 1))));
    ASSERT_EQ(nullptr, container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(1, 0))));
    ASSERT_EQ(nullptr, container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 2))));

    ASSERT_NE(nullptr, container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 0))));
    ASSERT_NE(nullptr, container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 0))));
    ASSERT_NE(nullptr, container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 1))));
    ASSERT_NE(nullptr, container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 1))));
    ASSERT_EQ(nullptr, container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 2))));
    ASSERT_EQ(nullptr, container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(2, 0))));

    *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget1, Vec2D(0, 0))) = 10;
    ASSERT_EQ(10, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget1, Vec2D(0, 0))));
}

TEST(WidgetTopologyContainerTest, EmptyTest) {
    WidgetTopologyContainer<int, TestEmptyWidgetTopology> emptyContainer;
    ASSERT_EQ(0, sizeof(emptyContainer));
    ASSERT_EQ(nullptr, emptyContainer.get(Widget<TestEmptyWidgetTopology>(TestEmptyWidgetTopology::WidgetId::Last, Vec2D(0, 0))));
}

class Visitor
{
public:
    void operator()(int& val, const Widget<TestWidgetTopology>& widget)
    {
        val = widget.coord.x * 10 + widget.coord.y;
    }
};

TEST(WidgetTopologyContainerTest, ForEachTest) {
    WidgetTopologyContainer<int, TestWidgetTopology> container;
    container.forEach(Visitor());
    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget1, Vec2D(0, 0))));

    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 0))));
    ASSERT_EQ(1, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 1))));

    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 0))));
    ASSERT_EQ(10, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 0))));
    ASSERT_EQ(1, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 1))));
    ASSERT_EQ(11, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 1))));
}
