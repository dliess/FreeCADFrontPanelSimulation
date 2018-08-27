#include <cstdint> // uint8_t

template <class CallbackIf, unsigned int Size>
class CallbackStack
{
public:
    CallbackStack() :
        m_cb(),
        m_topIndex(0),
        m_botIndex(0)
    {}
    void pushBack(CallbackIf* pCbIf)
    {
        if(m_cb[m_topIndex])
        {
            incTopIndex();
        }
        m_cb[m_topIndex] = pCbIf;
    }
    CallbackIf* getActual() const
    {
        return m_cb[m_topIndex];
    }
    void remove(const CallbackIf* pCbIf)
    {
        uint8_t const tmpTopIndex = m_topIndex;
        if(m_cb[m_topIndex] == pCbIf)
        {
            m_cb[m_topIndex] = nullptr;
            decTopIndex();
        }
        for(uint8_t i = decIndex(tmpTopIndex); i != decIndex(m_botIndex); i = decIndex(i))
        {
            if(m_cb[i] == pCbIf)
            {
                for(uint8_t j = i; j != tmpTopIndex; j = incIndex(j))
                {
                    m_cb[j] = m_cb[incIndex(j)];
                    m_cb[incIndex(j)] = nullptr;
                }
                decTopIndex();
            }
        }
    }
private:
    CallbackIf* m_cb[Size];
    int8_t  m_topIndex;
    int8_t  m_botIndex;
    void incTopIndex()
    {
        m_topIndex = incIndex(m_topIndex); 
        if(m_topIndex == m_botIndex)
        { 
            m_botIndex = incIndex(m_botIndex);
        }
    }
    void decTopIndex()
    {
        if(m_topIndex != m_botIndex)
        {
            m_topIndex = decIndex(m_topIndex);
        }
    }
    uint8_t incIndex(uint8_t index)
    {
        ++index;
        if(index >= Size)
        {
            index=0;
        }
        return index;
    }
    uint8_t decIndex(uint8_t index)
    {
        if(index == 0)
        {
            index = Size - 1;
        }
        else
        {
            --index;
        }
        return index;
    }
};

template <class CallbackIf>
class CallbackStack<CallbackIf, 0>
{
};

template <class CallbackIf>
class CallbackStack<CallbackIf, 1>
{
public:
    CallbackStack() :
        m_cb(nullptr)
    {}
    void pushBack(CallbackIf* pCbIf)
    {
        m_cb = pCbIf;
    }
    CallbackIf* getActual() const
    {
        return m_cb;
    }
    void remove(const CallbackIf* pCbIf)
    {
        if(m_cb == pCbIf)
        {
            m_cb = nullptr;
        } 
    }
private:
    CallbackIf* m_cb;
};

template <class CallbackIf>
class CallbackStack<CallbackIf, 2>
{
public:
    CallbackStack() :
        m_cb{nullptr, nullptr}
    {}
    void pushBack(CallbackIf* pCbIf)
    {
        if(m_cb[1])
        {
            m_cb[0] = m_cb[1];
            m_cb[1] = pCbIf;
        }
        else if(m_cb[0])
        {
            m_cb[1] = pCbIf;
        }
        else
        {
            m_cb[0] = pCbIf;
        }
    }
    CallbackIf* getActual() const
    {
        if(m_cb[1])
        {
            return m_cb[1];
        }
        else
        {
            return m_cb[0];
        }
    }
    void remove(const CallbackIf* pCbIf)
    {
        if(m_cb[1] == pCbIf)
        {
            m_cb[1] = nullptr;
        }
        if(m_cb[0] == pCbIf)
        {
            m_cb[0] = m_cb[1];
            m_cb[0] = nullptr;
        }
    }
private:
    CallbackIf* m_cb[2];
};
