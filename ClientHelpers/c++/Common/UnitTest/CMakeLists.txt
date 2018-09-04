cmake_minimum_required(VERSION 2.6)
 
# Locate GTest
find_package(GTest REQUIRED)

set (CMAKE_CXX_STANDARD 11)

set(SOURCES "UT_main.cpp"
            "UT_WidgetTopologyContainer.cpp"
            "UT_IncrementHolder.cpp"
            "UT_ValueHolder.cpp"
            )
set(INCLUDE_DIRS
    "${CMAKE_CURRENT_SOURCE_DIR}/.."
    "${GTEST_INCLUDE_DIRS}")
 
# Link runTests with what we want to test and the GTest and pthread library
add_executable(runTestsCommon ${SOURCES})
target_include_directories(runTestsCommon PRIVATE ${INCLUDE_DIRS})
target_link_libraries(runTestsCommon ${GTEST_LIBRARIES} pthread)

