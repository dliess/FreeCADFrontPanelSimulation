#ifndef CALLBACK_CONTAINER_H
#define CALLBACK_CONTAINER_H

#include "WidgetTopologyContainer.h"
#include "WidgetTopology.h"
#include "CallbackStack.h"
#include "CallbackIf.h"

template <class WidgetType>
using CallbackContainer = WidgetTopologyContainer<CallbackStack<CallbackIf<WidgetType>, 3>, WidgetTopology<WidgetType> >;

#endif