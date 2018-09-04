cmake_minimum_required(VERSION 2.6)

add_subdirectory(UnitTest EXCLUDE_FROM_ALL)

set (CMAKE_CXX_STANDARD 11)

set(INCLUDE_DIRS
    "${PROJECT_SOURCE_DIR}")
 
add_library(FPIOHandler INTERFACE)
target_include_directories(FPIOHandler INTERFACE ${INCLUDE_DIRS})
target_link_libraries(FPIOHandler INTERFACE common)