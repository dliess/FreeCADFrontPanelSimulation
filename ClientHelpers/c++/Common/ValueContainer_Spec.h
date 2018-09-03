#ifndef VALUE_CONTAINER_SPEC_H
#define VALUE_CONTAINER_SPEC_H

#include "ValueContainer.h"
#include "WidgetTypes.h"

using PotValContainer   = ValueContainer<WidgetTypes::Potentiometer>;
using EncIncrContainer  = ValueContainer<WidgetTypes::Encoder>;
using BtnValContainer   = ValueContainer<WidgetTypes::Button>;
using TouchValContainer = ValueContainer<WidgetTypes::TouchSurface>;

#endif