 project(FoundationTimer)
 cmake_minimum_required(VERSION 2.8.12)
 add_definitions("-std=c++11")


if(NOT EXISTS "${CMAKE_SOURCE_DIR}/cmake/conan/conan.cmake")
  if (NOT EXISTS ${CMAKE_BINARY_DIR}/conan.cmake)
        message(STATUS "Downloading conan.cmake from https://github.com/memsharded/cmake-conan")
        file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/master/conan.cmake"
                "${CMAKE_BINARY_DIR}/conan.cmake"
                SHOW_PROGRESS STATUS status)
        message(STATUS "Download status = ${status}")
  else ()
        message (STATUS "Using existing ${CMAKE_BINARY_DIR}/conan.cmake")
  endif ()
  include(${CMAKE_BINARY_DIR}/conan.cmake)
else()
  include(${CMAKE_SOURCE_DIR}/cmake/conan/conan.cmake)
endif ()
 
conan_cmake_run(CONANFILE conanfile.txt 
  BASIC_SETUP CMAKE_TARGETS
  BUILD missing)

conan_load_buildinfo ()

conan_basic_setup(NO_OUTPUT_DIRS)

 add_executable(tut01 tut01.cpp)
 target_link_libraries(tut01 CONAN_PKG::SDL2)
 
