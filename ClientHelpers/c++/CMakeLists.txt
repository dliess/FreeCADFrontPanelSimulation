cmake_minimum_required(VERSION 2.6)
 
set (CMAKE_CXX_STANDARD 11)

project(ClientHelper C CXX)

add_subdirectory(Common)
add_subdirectory(HAL)
add_subdirectory(FPIOHandlers)

add_custom_target(runTests)
add_dependencies(runTests runTestsCommon runTestsFpIO)