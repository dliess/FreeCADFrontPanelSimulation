#ifndef CALLBACK_CONTAINER_H
#define CALLBACK_CONTAINER_H

#include "WidgetTopologyContainer.h"
#include "WidgetTopology.h"
#include "CallbackStack.h"
#include "CallbackIf.h"
#include "WidgetTypes.h"

template <class WidgetType>
using CallbackContainer = WidgetTopologyContainer<CallbackStack<CallbackIf<WidgetType>, 3>, WidgetTopology<WidgetType> >;

using PotCbContainer   = CallbackContainer<WidgetTypes::Potentiometer>;
using EncCbContainer  = CallbackContainer<WidgetTypes::Encoder>;
using BtnCbContainer   = CallbackContainer<WidgetTypes::Button>;
using TouchCbContainer = CallbackContainer<WidgetTypes::TouchSurface>;


#endif