template <class DataType, class WidgetFunction>
class WidgetTopologyContainer
{
public:
    WidgetTopologyContainer()
    {
        for(int i = 0; i <=  WidgetFunction::WidgetId::Last, ++i)
        {
            m_holder[i] = new DataType[WidgetFunction::getDim[i].x * WidgetFunction::getDim[i].y]
        }
    }
    ~WidgetTopologyContainer()
    {
        for(int i = 0; i <=  WidgetFunction::WidgetId::Last, ++i)
        {
            delete m_holder[i];
        }
    }

    DataType *get(WidgetFunction::WidgetId widgetId, uint8_t x, uint8_t y)
    {
        if(x >= WidgetFunction::getDim[i].x || y >= WidgetFunction::getDim[i].y)
        {
            return nullptr;
        }
        return &(m_holder[widgetId][x * WidgetFunction::getDim[i].y + y]);
    }

    template<WidgetFunction::WidgetId WidgetId>
    DataType *get<WidgetId>(const WidgetTraits<WidgetId>::Coord& coord)
    {
        if(x >= WidgetFunction::getDim[i].x || y >= WidgetFunction::getDim[i].y)
        {
            return nullptr;
        }
        return &(m_holder[widgetId][x * WidgetFunction::getDim[i].y + y]);
    }

private:
    DataType* m_holder[WidgetFunction::WidgetId::Last+1];
};