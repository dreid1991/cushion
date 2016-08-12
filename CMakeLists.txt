cmake_minimum_required (VERSION 2.6)
project (networks)
#note that Boost and PYTHON are case-sensitive
find_package (PythonLibs 2.7 REQUIRED)
include_directories (${PYTHON_INCLUDE_DIRS})

find_package (Boost COMPONENTS python REQUIRED)

file (GLOB SOURCES "*.cpp")
list (REMOVE_ITEM SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/main.cpp")
#REMEMBER OPT FLAGS
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -fpic ")

set (CUSHION_LIB_NAME Cush)

add_library(${CUSHION_LIB_NAME} SHARED ${SOURCES} )
target_link_libraries(${CUSHION_LIB_NAME} ${PYTHON_LIBRARIES} ${Boost_LIBRARIES})
#add_executable(main_exec main.cpp)
#target_link_libraries (main_exec ${CUSHION_LIB_NAME})

#build python shared library
set (PY_INC_DIRS ${CMAKE_CURRENT_SOURCE_DIR})

add_subdirectory (python)
