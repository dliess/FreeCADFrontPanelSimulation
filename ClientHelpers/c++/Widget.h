#ifndef WIDGET_H
#define WIDGET_H

#include <cstdint>
#include "Vector2D.h"

template<class WidgetTopology>
struct Widget
{
    using WidgetId = typename WidgetTopology::WidgetId;
    Widget(const WidgetId& _id, const Vec2D& _vec) :
       id(_id),
       coord(_vec)
    {}
    WidgetId id;
    Vec2D    coord;
};

#endif
