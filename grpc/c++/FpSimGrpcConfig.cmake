get_filename_component(FpSimGrpc_CMAKE_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
include(CMakeFindDependencyMacro)

find_dependency(Boost 1.55 REQUIRED COMPONENTS regex)
find_dependency(RapidJSON 1.0 REQUIRED MODULE)

if(NOT TARGET FpSimGrpc::FpSimGrpc)
    include("${FpSimGrpc_CMAKE_DIR}/FpSimGrpcTargets.cmake")
endif()
