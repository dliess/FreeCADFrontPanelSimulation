#ifndef VECTOR_2D_H
#define VECTOR_2D_H

#include <cstdint>
#include <limits>

template<typename T>
struct Vector2D
{
    Vector2D() :
        x(0),
        y(0)
    {}
    Vector2D(const Vector2D& other) :
        x(other.x),
        y(other.y)
    {}
    Vector2D(const T& _x, const T& _y) :
        x(_x),
        y(_y)
    {}
    bool operator!=(const Vector2D<T>& rhs) const
    {
        return (x != rhs.x) || (y != rhs.y);
    }
    bool operator==(const Vector2D<T>& rhs) const
    {
        return (x == rhs.x) && (y == rhs.y);
    }
    Vector2D& operator=(const T& val)
    {
        x = val;
        y = val;
        return *this;
    }
    Vector2D operator+(const Vector2D<T>& rhs) const
    {
        return Vector2D(x + rhs.x, y + rhs.y);
    }
    Vector2D inc() const
    {
        return Vector2D(x+1, y+1);
    }
    T x;
    T y;
    static const T ALL;
};

// This makes linker happy
template<typename T>
const T Vector2D<T>::ALL = std::numeric_limits<T>::max();


using Vec2D = Vector2D<uint8_t>;

#endif