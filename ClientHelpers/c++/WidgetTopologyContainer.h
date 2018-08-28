#include <cstdint>

template <class DataType, class WidgetFunction>
class WidgetTopologyContainer
{
public:
    WidgetTopologyContainer()
    {
        for(int i = 0; i <=  static_cast<int>(WidgetFunction::WidgetId::Last); ++i)
        {
            const typename WidgetFunction::WidgetId wId = static_cast<typename WidgetFunction::WidgetId>(i);
            m_holder[i] = new DataType[WidgetFunction::getDim(wId).x * WidgetFunction::getDim(wId).y];
        }
    }
    ~WidgetTopologyContainer()
    {
        for(int i = 0; i <=  WidgetFunction::WidgetId::Last; ++i)
        {
            delete m_holder[i];
        }
    }

    DataType *get(const typename WidgetFunction::WidgetId &widgetId, uint8_t x, uint8_t y)
    {
        if(x >= WidgetFunction::getDim(widgetId).x || y >= WidgetFunction::getDim(widgetId).y)
        {
            return nullptr;
        }
        return &(m_holder[widgetId][x * WidgetFunction::getDim(widgetId).y + y]);
    }
private:
    DataType* m_holder[WidgetFunction::WidgetId::Last+1];
};
