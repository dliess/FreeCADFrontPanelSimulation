#ifndef WIDGET_TOPOLOGY_CONTAINER_H
#define WIDGET_TOPOLOGY_CONTAINER_H

#include <cstdint>
#include "Widget.h"


template <class DataType, class WidgetTopology>
class WidgetTopologyContainer
{
public:
    WidgetTopologyContainer()
    {
        for(int i = 0; i <=  static_cast<int>(WidgetTopology::WidgetId::Last); ++i)
        {
            const typename WidgetTopology::WidgetId wId = static_cast<typename WidgetTopology::WidgetId>(i);
            m_holder[i] = new DataType[WidgetTopology::getDim(wId).x * WidgetTopology::getDim(wId).y];
        }
    }
    ~WidgetTopologyContainer()
    {
        for(int i = 0; i <=  WidgetTopology::WidgetId::Last; ++i)
        {
            delete m_holder[i];
        }
    }

    DataType *get(const Widget<WidgetTopology> &widgetPos)
    {
        if(widgetPos.coord.x >= WidgetTopology::getDim(widgetPos.id).x || widgetPos.coord.y >= WidgetTopology::getDim(widgetPos.id).y)
        {
            return nullptr;
        }
        return &(m_holder[widgetPos.id][widgetPos.coord.x * WidgetTopology::getDim(widgetPos.id).y + widgetPos.coord.y]);
    }

    template<class Visitor>
    void forEach(Visitor&& visitor)
    {
        for(int i = 0; i <=  static_cast<int>(WidgetTopology::WidgetId::Last); ++i)
        {
            const typename WidgetTopology::WidgetId wId = static_cast<typename WidgetTopology::WidgetId>(i);
            const auto DIM = WidgetTopology::getDim(wId);
            for(uint8_t x = 0; x < DIM.x; ++x)
            {
                for(uint8_t y = 0; y < DIM.y; ++y)
                {
                    Widget<WidgetTopology> widget(wId, Vec2D(x, y));
                    DataType* data = get(widget);
                    if(data)
                    {
                        visitor(*data, widget);
                    }
                }
            }
        }
    }
private:
    DataType* m_holder[WidgetTopology::WidgetId::Last+1];
};

#endif