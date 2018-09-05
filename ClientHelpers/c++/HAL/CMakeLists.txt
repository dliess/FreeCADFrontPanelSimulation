cmake_minimum_required(VERSION 2.8)

list(APPEND CMAKE_PREFIX_PATH "~/.FreeCAD/Mod/FreeCADFrontPanelSimulation/grpc/c++")

find_package(FpSimGrpc CONFIG REQUIRED)

#project(HALFpSim C CXX)

set (CMAKE_CXX_STANDARD 11)

add_library(HALFpSim STATIC
   "HALFpSim.cpp"
)

target_link_libraries(HALFpSim
    FpSimGrpc
    common)