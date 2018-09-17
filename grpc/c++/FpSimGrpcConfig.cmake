get_filename_component(FpSimGrpc_CMAKE_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
include(CMakeFindDependencyMacro)

find_dependency(protobuf REQUIRED CONFIG)
find_dependency(gRPC  REQUIRED CONFIG)

if(NOT TARGET FpSimGrpc::FpSimGrpc)
    include("${FpSimGrpc_CMAKE_DIR}/FpSimGrpcTargets.cmake")
endif()
