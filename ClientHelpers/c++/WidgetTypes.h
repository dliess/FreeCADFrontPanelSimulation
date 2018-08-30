#ifndef WIDGET_TYPES_H
#define WIDGET_TYPES_H

#include "ValueHolder.h"
#include "IncrementHolder.h"
#include "Vector2D.h"
#include <cstdint>

namespace WidgetTypes
{

class Button
{
public:
    enum State
    {
        Released = 0,
        Pressed  = 1
    };
    using ValueType      = State;
    using ValueHolder    = ValueHolder<ValueType>;
};

class Potentiometer
{
public:
    using ValueType      = uint32_t;
    using ValueHolder    = ValueHolder<ValueType>;
};

class Encoder
{
public:
    using ValueType      = int32_t;
    using ValueHolder    = IncrementHolder<ValueType>;
};

class TouchSurface
{
public:
    using ValueType      = Vector2D<uint32_t>;
    using ValueHolder    = ValueHolder<ValueType>;
};


} //namespace WidgetTypes
#endif