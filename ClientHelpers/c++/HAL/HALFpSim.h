#ifndef HAL_FP_SIM_H
#define HAL_FP_SIM_H

#include "ValueContainer_Spec.h"

class HALFpSim
{
public:
    void update(PotValContainer& container);
    void update(EncIncrContainer& container);
    void update(BtnValContainer& container);
    void update(TouchValContainer& container);
};

#endif