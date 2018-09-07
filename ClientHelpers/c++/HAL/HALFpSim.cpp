#include "HALFpSim.h"

void HALFpSim::update(PotValContainer& container)
{
    /*
    std::vector changedPotVals;
    changedPotVals = m_grpcClient.requestPotValues();
    for(auto it = begin (vector); it != end (vector); ++it)
    {
        auto widgetId = m_mapper.mapLabelToId(it->label);
        auto pValueHandler = container.get(widgetId);
        if(pValueHandler)
        {
            pValueHandler->set(it->value);
        }
    }
    */
}

void HALFpSim::update(EncIncrContainer& container){};
void HALFpSim::update(BtnValContainer& container){};
void HALFpSim::update(TouchValContainer& container){};
