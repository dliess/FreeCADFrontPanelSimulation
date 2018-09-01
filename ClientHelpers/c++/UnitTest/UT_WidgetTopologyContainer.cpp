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
    Visitor(int val) : m_val(val) {}
    void operator()(int& val, const Widget<TestWidgetTopology>& widget)
    {
        val = m_val;
    }
private:
    int m_val;
};

TEST(WidgetTopologyContainerTest, ForEachTest) {
    WidgetTopologyContainer<int, TestWidgetTopology> container;
    static const int VALUE = 1234;
    container.forEach(Visitor(VALUE));
    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget1, Vec2D(0, 0))));

    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 0))));
    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 1))));

    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 0))));
    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 0))));
    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 1))));
    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 1))));
}

TEST(WidgetTopologyContainerTest, ForWidgetTest) {
    WidgetTopologyContainer<int, TestWidgetTopology> container;
    Widget<TestWidgetTopology> widget(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 1));

    container.forEach(Visitor(0));
    static const int VALUE = 1234;
    container.forWidget(widget, Visitor(VALUE));

    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget1, Vec2D(0, 0))));

    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 0))));
    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 1))));

    ASSERT_EQ(0,     *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 0))));
    ASSERT_EQ(0,     *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 0))));
    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 1))));
    ASSERT_EQ(0,     *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 1))));

    container.forEach(Visitor(0));
    widget.coord.x = widget.coord.ALL;
    widget.coord.y = 1;
    container.forWidget(widget, Visitor(VALUE));

    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget1, Vec2D(0, 0))));

    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 0))));
    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 1))));

    ASSERT_EQ(0,     *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 0))));
    ASSERT_EQ(0,     *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 0))));
    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 1))));
    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 1))));

    container.forEach(Visitor(0));
    widget.coord.x = 0;
    widget.coord.y = widget.coord.ALL;
    container.forWidget(widget, Visitor(VALUE));

    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget1, Vec2D(0, 0))));

    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 0))));
    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 1))));

    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 0))));
    ASSERT_EQ(0,     *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 0))));
    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 1))));
    ASSERT_EQ(0,     *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 1))));

    container.forEach(Visitor(0));
    widget.coord.x = widget.coord.ALL;
    widget.coord.y = widget.coord.ALL;
    container.forWidget(widget, Visitor(VALUE));

    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget1, Vec2D(0, 0))));

    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 0))));
    ASSERT_EQ(0, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget2, Vec2D(0, 1))));

    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 0))));
    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 0))));
    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(0, 1))));
    ASSERT_EQ(VALUE, *container.get(Widget<TestWidgetTopology>(TestWidgetTopology::WidgetId::Widget3, Vec2D(1, 1))));
}