cmake_minimum_required(VERSION 3.12)
project(RIME C)

set(CMAKE_C_STANDARD 11)

include_directories(back_end/c)

add_library(parserlib SHARED back_end/c/parser.c back_end/c/parser.h back_end/c/hash_table.c)

add_executable(RIME
        back_end/c/parser_test.c
        back_end/c/status_updater.c
        back_end/c/status_updater.h back_end/c/netCDF.c back_end/c/dum_cdf.c back_end/c/hash_table.h)

target_link_libraries(RIME LINK_PUBLIC parserlib)