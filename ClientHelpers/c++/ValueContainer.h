#ifndef VALUE_CONTAINER_H
#define VALUE_CONTAINER_H

#include "WidgetTopologyContainer.h"

template <class WidgetType>
using ValueContainer = WidgetTopologyContainer<typename WidgetType::ValueHolder, WidgetType>;

#endif