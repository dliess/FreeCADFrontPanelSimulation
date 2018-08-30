#ifndef INCREMENT_HOLDER_H
#define INCREMENT_HOLDER_H

template< class T >
class IncrementHolder
{
public:
    IncrementHolder() : 
        m_increment()
    {}

    void set(const T& increment)
    {
        m_increment = increment;
    }

    const T& value() const
    {
        return m_increment;
    }

    bool hasChanged() const
    {
        return 0 != m_increment;
    }

    void resetState()
    {
        m_increment = 0;
    }

private:
    T m_increment;
};

#endif