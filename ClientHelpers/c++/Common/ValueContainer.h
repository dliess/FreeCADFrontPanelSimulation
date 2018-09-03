#ifndef VALUE_CONTAINER_H
#define VALUE_CONTAINER_H

#include "WidgetTopologyContainer.h"
#include "WidgetTypes.h"
#include "WidgetTopology.h"

template <class WidgetType>
using ValueContainer = WidgetTopologyContainer<typename WidgetType::ValueHandler, WidgetTopology<WidgetType> >;

#endif