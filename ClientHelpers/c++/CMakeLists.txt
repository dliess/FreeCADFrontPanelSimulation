cmake_minimum_required(VERSION 2.6)
 
set (CMAKE_CXX_STANDARD 11)

set(INCLUDE_DIRS
    "${PROJECT_SOURCE_DIR}")
 
add_library(clientHelper INTERFACE)
target_include_directories(clientHelper INTERFACE ${INCLUDE_DIRS})
