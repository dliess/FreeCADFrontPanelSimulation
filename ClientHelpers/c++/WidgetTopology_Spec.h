#ifndef WIDGET_TOPOLOGY_SPEC_H
#define WIDGET_TOPOLOGY_SPEC_H

#include "WidgetTypes.h"
#include "WidgetTopology.h"

using PotId = WidgetTopology<WidgetTypes::Potentiometer>::WidgetId;
using EncId = WidgetTopology<WidgetTypes::Encoder>::WidgetId;
using BtnId = WidgetTopology<WidgetTypes::Button>::WidgetId;
using TouchId = WidgetTopology<WidgetTypes::TouchSurface>::WidgetId;

#endif