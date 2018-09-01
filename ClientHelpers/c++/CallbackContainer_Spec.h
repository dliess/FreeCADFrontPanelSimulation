#ifndef CALLBACK_CONTAINER_SPEC_H
#define CALLBACK_CONTAINER_SPEC_H

#include "CallbackContainer.h"
#include "WidgetTypes.h"

using PotCbContainer   = CallbackContainer<WidgetTypes::Potentiometer>;
using EncCbContainer  = CallbackContainer<WidgetTypes::Encoder>;
using BtnCbContainer   = CallbackContainer<WidgetTypes::Button>;
using TouchCbContainer = CallbackContainer<WidgetTypes::TouchSurface>;


#endif