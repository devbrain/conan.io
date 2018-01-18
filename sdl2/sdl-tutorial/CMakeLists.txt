 project(FoundationTimer)
 cmake_minimum_required(VERSION 2.8.12)
 add_definitions("-std=c++11")

 include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
 conan_basic_setup()

 add_executable(tut01 tut01.cpp)
 target_link_libraries(tut01 ${CONAN_LIBS})
 
