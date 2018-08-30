#ifndef VALUE_HOLDER_H
#define VALUE_HOLDER_H

template< class T >
class ValueHolder
{
public:
    ValueHolder() : 
        m_value(),
        m_hasChanged(true)
    {}

    void set(const T& newVal)
    {
        if( m_value != newVal)
        {
            m_hasChanged = true;
            m_value = newVal;
        }
    }

    const T& value() const
    {
        return m_value;
    }

    bool hasChanged() const
    {
        return m_hasChanged;
    }

    void resetState()
    {
        m_hasChanged = false;
    }

private:
    T m_value;
    bool m_hasChanged;
};

#endif