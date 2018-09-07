#ifndef WIDGET_TOPOLOGY_H
#define WIDGET_TOPOLOGY_H

#include "WidgetTypes.h"
#include "Vector2D.h"

template<class WidgetType>
class WidgetTopology
{
};

template<>
class WidgetTopology<WidgetTypes::Potentiometer>
{
public:
    enum WidgetId{
        Pot1       =  0,
        PotMatrix  =  1,
        Last       =  PotMatrix
    };
    static const Vec2D& getDim(WidgetId widgetId)
    {
        static const Vec2D dim[WidgetId::Last + 1] = {{1,1},{2,8}};
        return dim[widgetId];
    }
};

template<>
class WidgetTopology<WidgetTypes::Encoder>
{
public:
    enum WidgetId{
        EncMatrix = 0,
        Last      = EncMatrix
    };
    static const Vec2D& getDim(WidgetId widgetId)
    {
        static const Vec2D dim[WidgetId::Last + 1] = {{4,8}};
        return dim[widgetId];
    }
};

template<>
class WidgetTopology<WidgetTypes::Button>
{
public:
    enum WidgetId{
        Menu  = 0,
        Notes = 1,
        Last  = Notes
    };
    static const Vec2D& getDim(WidgetId widgetId)
    {
        static const Vec2D dim[WidgetId::Last + 1] = {{1,1},{1,24}};
        return dim[widgetId];
    }
};

template<>
class WidgetTopology<WidgetTypes::TouchSurface>
{
public:
    enum WidgetId{
        Touch1  =  0,
        Touch2  =  1,
        Touch3  =  2,
        Last    =  Touch3
    };
    static const Vec2D& getDim(WidgetId widgetId)
    {
        static const Vec2D dim[WidgetId::Last + 1] = {{1,1},{1,1},{1,1}};
        return dim[widgetId];
    }
};

#endif