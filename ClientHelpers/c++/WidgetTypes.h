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
    enum class State : uint8_t
    {
        Released = 0,
        Pressed  = 1
    };
    using ValueType      = State;
    using ValueHandler   = ValueHolder<ValueType>;
};

class Potentiometer
{
public:
    using ValueType      = uint32_t;
    using ValueHandler   = ValueHolder<ValueType>;
};

class Encoder
{
public:
    using ValueType      = int32_t;
    using ValueHandler   = IncrementHolder<ValueType>;
};

class TouchSurface
{
public:
    using ValueType      = Vector2D<uint32_t>;
    using ValueHandler   = ValueHolder<ValueType>;
};

} //namespace WidgetTypes

template<typename T>
void reset(T& val) {val = 0;}

template<>
void reset<WidgetTypes::Button::ValueType>(WidgetTypes::Button::ValueType& val)
{
    val = WidgetTypes::Button::State::Released;
}


#endif