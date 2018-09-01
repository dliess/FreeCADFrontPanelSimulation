#ifndef CALLBACK_IF_SPEC_H
#define CALLBACK_IF_SPEC_H

#include "CallbackIf.h"
#include "WidgetTypes.h"

using PotCallback   = CallbackIf<WidgetTypes::Potentiometer>;
using EncCallback   = CallbackIf<WidgetTypes::Encoder>;
using BtnCallback   = CallbackIf<WidgetTypes::Button>;
using TouchCallback = CallbackIf<WidgetTypes::TouchSurface>;

#endif