cmake_minimum_required(VERSION 2.8)

project(FpSimGrpcCpp C CXX)

set (CMAKE_CXX_STANDARD 11)
#if(NOT MSVC)
#  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
#else()
#  add_definitions(-D_WIN32_WINNT=0x600)
#endif()

if(GRPC_AS_SUBMODULE)
  # One way to build a projects that uses gRPC is to just include the
  # entire gRPC project tree via "add_subdirectory".
  # This approach is very simple to use, but the are some potential
  # disadvantages:
  # * it includes gRPC's CMakeLists.txt directly into your build script
  #   without and that can make gRPC's internal setting interfere with your
  #   own build.
  # * depending on what's installed on your system, the contents of submodules
  #   in gRPC's third_party/* might need to be available (and there might be
  #   additional prerequisites required to build them). Consider using
  #   the gRPC_*_PROVIDER options to fine-tune the expected behavior.
  #
  # A more robust approach to add dependency on gRPC is using
  # cmake's ExternalProject_Add (see cmake_externalproject/CMakeLists.txt).
  
  # Include the gRPC's cmake build (normally grpc source code would live
  # in a git submodule called "third_party/grpc", but this example lives in
  # the same repository as gRPC sources, so we just look a few directories up)
  add_subdirectory(grpc grpc/build EXCLUDE_FROM_ALL)
  message(STATUS "Using gRPC via add_subdirectory.")
  
  # After using add_subdirectory, we can now use the grpc targets directly from
  # this build.
  set(_PROTOBUF_LIBPROTOBUF libprotobuf)
  set(_PROTOBUF_PROTOC $<TARGET_FILE:protoc>)
  set(_GRPC_GRPCPP_UNSECURE grpc++_unsecure)
  set(_GRPC_CPP_PLUGIN_EXECUTABLE $<TARGET_FILE:grpc_cpp_plugin>)
else()
  # This branch assumes that gRPC and all its dependencies are already installed
  # on this system, so they can be located by find_package().

  # Find Protobuf installation
  # Looks for protobuf-config.cmake file installed by Protobuf's cmake installation.
  set(protobuf_MODULE_COMPATIBLE TRUE)
  find_package(Protobuf CONFIG REQUIRED)
  message(STATUS "Using protobuf ${protobuf_VERSION}")

  set(_PROTOBUF_LIBPROTOBUF protobuf::libprotobuf)
  set(_PROTOBUF_PROTOC $<TARGET_FILE:protobuf::protoc>)

  # Find gRPC installation
  # Looks for gRPCConfig.cmake file installed by gRPC's cmake installation.
  find_package(gRPC CONFIG REQUIRED)
  message(STATUS "Using gRPC ${gRPC_VERSION}")

  set(_GRPC_GRPCPP_UNSECURE gRPC::grpc++_unsecure)
  set(_GRPC_CPP_PLUGIN_EXECUTABLE $<TARGET_FILE:gRPC::grpc_cpp_plugin>)
endif()

# Proto file
get_filename_component(hw_proto "../FPSimulation.proto" ABSOLUTE)
get_filename_component(hw_proto_path "${hw_proto}" PATH)
get_filename_component(hw_proto_basename "${hw_proto}" NAME_WE)

# Generated sources
set(hw_proto_srcs "${CMAKE_CURRENT_BINARY_DIR}/${hw_proto_basename}.pb.cc")
set(hw_proto_hdrs "${CMAKE_CURRENT_BINARY_DIR}/${hw_proto_basename}.pb.h")
set(hw_grpc_srcs "${CMAKE_CURRENT_BINARY_DIR}/${hw_proto_basename}.grpc.pb.cc")
set(hw_grpc_hdrs "${CMAKE_CURRENT_BINARY_DIR}/${hw_proto_basename}.grpc.pb.h")
add_custom_command(
      OUTPUT "${hw_proto_srcs}" "${hw_proto_hdrs}" "${hw_grpc_srcs}" "${hw_grpc_hdrs}"
      COMMAND ${_PROTOBUF_PROTOC}
      ARGS --grpc_out "${CMAKE_CURRENT_BINARY_DIR}"
        --cpp_out "${CMAKE_CURRENT_BINARY_DIR}"
        -I "${hw_proto_path}"
        --plugin=protoc-gen-grpc="${_GRPC_CPP_PLUGIN_EXECUTABLE}"
        "${hw_proto}"
      DEPENDS "${hw_proto}")

add_library(FpSimGrpc STATIC
  ${hw_proto_srcs}
  ${hw_grpc_srcs}
  GrpcClient.cpp
)

target_include_directories(FpSimGrpc
    PUBLIC
        $<INSTALL_INTERFACE:include>    
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)

target_link_libraries(FpSimGrpc
  ${_GRPC_GRPCPP_UNSECURE}
  ${_PROTOBUF_LIBPROTOBUF}
)

set_target_properties(FpSimGrpc PROPERTIES PUBLIC_HEADER "GrpcClient.h;${hw_grpc_hdrs};${hw_proto_hdrs}")

include(GNUInstallDirs)
install(TARGETS FpSimGrpc
    EXPORT FpSimGrpc-targets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)
install(FILES FpSimGrpcConfig.cmake DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/FpSimGrpc)

install(EXPORT FpSimGrpc-targets
  FILE
    FpSimGrpcTargets.cmake
  NAMESPACE
    FpSimGrpc::
  DESTINATION
    ${CMAKE_INSTALL_LIBDIR}/cmake/FpSimGrpc
)