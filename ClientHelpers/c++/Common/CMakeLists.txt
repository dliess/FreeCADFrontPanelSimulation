cmake_minimum_required(VERSION 2.6)
 
set (CMAKE_CXX_STANDARD 11)

set(TOPOLOGY_HEADER "${CMAKE_CURRENT_SOURCE_DIR}/WidgetTopology.h")
add_custom_command(
    OUTPUT "${TOPOLOGY_HEADER}"
    COMMAND PYTHONPATH=${PROJECT_SOURCE_DIR}/../.. python ${CMAKE_CURRENT_SOURCE_DIR}/Topology/WidgetCodeGenerator.py WidgetTopology.json
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/Topology
    COMMENT "Generating Widget-Topology header"
    DEPENDS "Topology/WidgetTopology.json")

add_custom_target(generateTopologyHeader DEPENDS "${TOPOLOGY_HEADER}")

set(INCLUDE_DIRS
    "${CMAKE_CURRENT_SOURCE_DIR}"
    "${CMAKE_CURRENT_SOURCE_DIR}/Topology"
    )

add_library(clientHelperCommon INTERFACE)
target_include_directories(clientHelperCommon INTERFACE ${INCLUDE_DIRS})
add_dependencies(clientHelperCommon generateTopologyHeader)