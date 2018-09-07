cmake_minimum_required(VERSION 2.6)

add_subdirectory(UnitTest EXCLUDE_FROM_ALL)

set (CMAKE_CXX_STANDARD 11)

set(TOPOLOGY_DIR "${CMAKE_CURRENT_SOURCE_DIR}/Topology")
set(TOPOLOGY_GENERATED_HEADER "${TOPOLOGY_DIR}/WidgetTopology.h")
set(TOPOLOGY_SOURCE_JSON "${TOPOLOGY_DIR}/WidgetTopology.json")
set(TOPOLOGY_CODE_GEN_TOOL "${CMAKE_CURRENT_LIST_DIR}/Topology/WidgetCodeGenerator.py")
set(FPSIM_PLUGIN_DIR "$ENV{HOME}/.FreeCAD/Mod/FreeCADFrontPanelSimulation")

add_custom_command(
    OUTPUT ${TOPOLOGY_GENERATED_HEADER}
    COMMAND PYTHONPATH=${FPSIM_PLUGIN_DIR} python ${TOPOLOGY_CODE_GEN_TOOL} ${TOPOLOGY_SOURCE_JSON}
    WORKING_DIRECTORY ${TOPOLOGY_DIR}
    COMMENT "Generating Widget-Topology header"
    DEPENDS ${TOPOLOGY_SOURCE_JSON})

add_custom_target(generateTopologyHeader DEPENDS "${TOPOLOGY_GENERATED_HEADER}")

set(INCLUDE_DIRS
    "${CMAKE_CURRENT_LIST_DIR}"
    "${TOPOLOGY_DIR}"
    )

add_library(topology INTERFACE)
target_include_directories(topology INTERFACE ${INCLUDE_DIRS})
add_dependencies(topology generateTopologyHeader)