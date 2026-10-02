cmake_minimum_required(VERSION 3.20)
project(Engine VERSION 1.0 LANGUAGES CXX)
add_executable(engine WIN32 main.cpp)
target_compile_features(engine PRIVATE cxx_std_20)
target_compile_options(engine PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:-Wall -Wextra -Wpedantic -Werror>
    $<$<CXX_COMPILER_ID:MSVC>:/WX>
)
target_link_options(engine PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/ENTRY:mainCRTStartup>
)