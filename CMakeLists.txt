cmake_minimum_required(VERSION 3.12)
project(BoyerMoore)

find_package(pybind11 REQUIRED)

pybind11_add_module(libboyer_moore boyer_moore.cpp)

# Link against pybind11
target_link_libraries(libboyer_moore PRIVATE pybind11::module)

