#include "WidgetTopology.h"
#include "WidgetTypes.h"

template<>
class WidgetTopology<WidgetTypes::Potentiometer>
{
public:
    enum WidgetId{
        Last    = -1
    };
   static const Vec2D& getDim(WidgetId widgetId)
   {
      static const Vec2D dim = {0,0};
      return dim;
   }
};

template<>
class WidgetTopology<WidgetTypes::Encoder>
{
public:
    enum WidgetId{
        Last    = -1
    };
   static const Vec2D& getDim(WidgetId widgetId)
   {
      static const Vec2D dim = {0,0};
      return dim;
   }
};

template<>
class WidgetTopology<WidgetTypes::Button>
{
public:
    enum WidgetId{
        Last    = -1
    };
   static const Vec2D& getDim(WidgetId widgetId)
   {
      static const Vec2D dim = {0,0};
      return dim;
   }
};

template<>
class WidgetTopology<WidgetTypes::TouchSurface>
{
public:
    enum WidgetId{
        Last    = -1
    };
   static const Vec2D& getDim(WidgetId widgetId)
   {
      static const Vec2D dim = {0,0};
      return dim;
   }
};

#include <gtest/gtest.h>
#include "FpInputHandler.h" //important to include it after topology classes


class TestFpHal
{
public:
    void update(PotValContainer& container){};
    void update(EncIncrContainer& container){};
    void update(BtnValContainer& container){};
    void update(TouchValContainer& container){};
};


TEST(FpInputHandlerTest, Run) {
    TestFpHal hal;
    FpInputHandler<TestFpHal> fpInputHandler(hal);
    fpInputHandler.poll();
}