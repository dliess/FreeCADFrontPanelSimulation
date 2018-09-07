#ifndef WIDGET_SPEC_H
#define WIDGET_SPEC_H

#include "Widget.h"
#include "WidgetTypes.h"
#include "WidgetTopology.h"

using PotWidget   = Widget< WidgetTopology<WidgetTypes::Potentiometer> >;
using EncWidget   = Widget< WidgetTopology<WidgetTypes::Encoder> >;
using BtnWidget   = Widget< WidgetTopology<WidgetTypes::Button> >;
using TouchWidget = Widget< WidgetTopology<WidgetTypes::TouchSurface> >;

#endif