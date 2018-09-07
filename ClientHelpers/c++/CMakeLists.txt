cmake_minimum_required(VERSION 2.6)
 
set (CMAKE_CXX_STANDARD 11)

project(ClientHelper C CXX)

add_subdirectory(Topology)
add_subdirectory(HAL)
add_subdirectory(FrontPanelIO)

add_custom_target(UnitTests)
add_dependencies(UnitTests runTestsCommon runTestsFpIO)