cmake_minimum_required(VERSION 2.6)
 
# Locate GTest
find_package(GTest REQUIRED)

set (CMAKE_CXX_STANDARD 11)

set(SOURCES "UT_main.cpp"
            "UT_CallbackStack.cpp"
            "UT_ValueChangeHandler.cpp"
            "UT_FpInputHandler/UT_FpInputHandler.cpp"
            )
set(INCLUDE_DIRS
    "${PROJECT_SOURCE_DIR}/.."
    "${PROJECT_SOURCE_DIR}/UT_FpInputHandler"
    "${GTEST_INCLUDE_DIRS}")
 
# Link runTests with what we want to test and the GTest and pthread library
add_executable(runTests ${SOURCES})
target_include_directories(runTests PRIVATE ${INCLUDE_DIRS})
target_link_libraries(runTests ${GTEST_LIBRARIES} pthread)

