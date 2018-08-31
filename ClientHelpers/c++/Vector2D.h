#ifndef VECTOR_2D_H
#define VECTOR_2D_H

#include <cstdint>

template<typename T>
struct Vector2D
{
    Vector2D() :
        x(0),
        y(0)
    {}
    Vector2D(const T& _x, const T& _y) :
        x(_x),
        y(_y)
    {}
    T x;
    T y;
};

typedef Vector2D<uint8_t> Vec2D;

#endif