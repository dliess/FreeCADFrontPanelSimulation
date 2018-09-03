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

class Display
{};

class Led
{};

class PotentiometerMove
{};

} //namespace WidgetTypes

using PotValue   = WidgetTypes::Potentiometer::ValueType;
using EncValue   = WidgetTypes::Encoder::ValueType;
using BtnValue   = WidgetTypes::Button::ValueType;
using TouchValue = WidgetTypes::TouchSurface::ValueType;


#endif