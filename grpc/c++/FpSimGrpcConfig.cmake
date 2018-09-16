get_filename_component(FpSimGrpc_CMAKE_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
include(CMakeFindDependencyMacro)

#find_dependency(grpc REQUIRED MODULE)
find_dependency(Protobuf CONFIG REQUIRED)
find_dependency(gRPC CONFIG REQUIRED)


if(NOT TARGET FpSimGrpc::FpSimGrpc)
    include("${FpSimGrpc_CMAKE_DIR}/FpSimGrpcTargets.cmake")
endif()

set_target_properties(FpSimGrpc::FpSimGrpc PROPERTIES IMPORTED_LINK_INTERFACE_LIBRARIES gRpc Protobuf)
