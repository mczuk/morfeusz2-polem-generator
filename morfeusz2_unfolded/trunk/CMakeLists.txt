
cmake_minimum_required (VERSION 2.8) 
project (Morfeusz)

set (Morfeusz_VERSION_MAJOR 2)
set (Morfeusz_VERSION_MINOR 0)
set (Morfeusz_VERSION_PATCH 0)
set (Morfeusz_VERSION "${Morfeusz_VERSION_MAJOR}.${Morfeusz_VERSION_MINOR}.${Morfeusz_VERSION_PATCH}")
if (DEFAULT_DICT_NAME)
    set (Morfeusz_VERSION_TWEAK "${DEFAULT_DICT_NAME}")
    if (DICT_VERSION)
        set (Morfeusz_VERSION_TWEAK "${Morfeusz_VERSION_TWEAK}.${DICT_VERSION}")
    endif()
    set (Morfeusz_VERSION "${Morfeusz_VERSION}.${Morfeusz_VERSION_TWEAK}")
    if (NOT DICT_VERSION)
        set (DICT_VERSION "1.0")
        message (WARNING "Dictionary version is missing. Setting default value=1.0")
    endif()

set (CPACK_PACKAGE_VERSION "${Morfeusz_VERSION}")
    
elseif (INPUT_DICTIONARIES)
    message (FATAL_ERROR "DEFAULT_DICT_NAME option is missing.")
elseif (NOT SKIP_DICTIONARY_BUILDING)
    message (WARNING "Will build WITHOUT DICTIONARY. Set INPUT_DICTIONARIES option to build with dictionary.")
endif ()

if (NOT CMAKE_BUILD_TYPE)
    set (CMAKE_BUILD_TYPE Release)
endif ()
#~ set (CMAKE_SKIP_RPATH ON)

message ("Version=${Morfeusz_VERSION}")

#if ( (NOT "${CMAKE_SYSTEM_NAME}" MATCHES "Linux") OR ((NOT INPUT_DICTIONARIES) AND NOT (SKIP_DICTIONARY_BUILDING)))
#    set (EMBEDDED_DEFAULT_DICT 1)
#    message (WARNING "Implicitly setting EMBEDDED_DEFAULT_DICT variable to TRUE")
#endif ()

if ( (NOT "${CMAKE_SYSTEM_NAME}" MATCHES "Linux") OR ((NOT INPUT_DICTIONARIES) AND NOT (SKIP_DICTIONARY_BUILDING)))
    set (EMBEDDED_DEFAULT_DICT 1)
    message (WARNING "Implicitly setting EMBEDDED_DEFAULT_DICT variable to TRUE")
endif ()

# INPUT_DICTIONARY_CPP
if (EMBEDDED_DEFAULT_DICT)
    if (NOT ANALYZER_DICTIONARY_CPP)
        set (ANALYZER_DICTIONARY_CPP "default_fsa.cpp")
    endif ()
    if (NOT GENERATOR_DICTIONARY_CPP)
        set (GENERATOR_DICTIONARY_CPP "default_synth_fsa.cpp")
    endif ()
else ()
    if (NOT DEFAULT_DICT_DIR)
        set (DEFAULT_DICT_DIR "${CMAKE_CURRENT_BINARY_DIR}/morfeusz")
    endif ()
    set (DEFAULT_DICT_INSTALL_DIR "share/morfeusz/dictionaries")
endif ()

add_definitions (-DMORFEUSZ2_VERSION="${Morfeusz_VERSION_MAJOR}.${Morfeusz_VERSION_MINOR}.${Morfeusz_VERSION_PATCH}")
add_definitions (-DMORFEUSZ_DEFAULT_DICT_NAME="${DEFAULT_DICT_NAME}")
add_definitions (-DBUILDING_MORFEUSZ)
if (EMBEDDED_DEFAULT_DICT)
    add_definitions (-DMORFEUSZ_EMBEDDED_DEFAULT_DICT )
else ()
    if ("${CMAKE_INSTALL_PREFIX}" STREQUAL "/usr" OR "${CMAKE_INSTALL_PREFIX}" STREQUAL "/usr/local")
        add_definitions (-DMORFEUSZ_DICTIONARY_SEARCH_PATH1="/usr/local/${DEFAULT_DICT_INSTALL_DIR}")
        add_definitions (-DMORFEUSZ_DICTIONARY_SEARCH_PATH2="/usr/${DEFAULT_DICT_INSTALL_DIR}")
    else ()
        add_definitions (-DMORFEUSZ_DICTIONARY_SEARCH_PATH1="${CMAKE_INSTALL_PREFIX}/${DEFAULT_DICT_INSTALL_DIR}")
        add_definitions (-DMORFEUSZ_DICTIONARY_SEARCH_PATH2="/usr/local/${DEFAULT_DICT_INSTALL_DIR}")
        add_definitions (-DMORFEUSZ_DICTIONARY_SEARCH_PATH3="/usr/${DEFAULT_DICT_INSTALL_DIR}")
    endif ()
endif ()

if (NOT CMAKE_CROSSCOMPILING AND NOT SKIP_TESTING)
    enable_testing()
endif ()

##### initialize some vars #####

# ARCHITECTURE
if ("${CMAKE_SYSTEM_PROCESSOR}" STREQUAL "x86_64")
    set (ARCHITECTURE "amd64")
elseif ("${CMAKE_SYSTEM_PROCESSOR}" STREQUAL "x86")
    set (ARCHITECTURE "i386")
elseif ("${CMAKE_SYSTEM_PROCESSOR}" STREQUAL "")
    message (FATAL_ERROR "CMAKE_SYSTEM_PROCESSOR is not set (should be x86 or x86_64)")
elseif (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    set (ARCHITECTURE "amd64")
else ()
    set (ARCHITECTURE "${CMAKE_SYSTEM_PROCESSOR}")
#    message (FATAL_ERROR "Invalid architecture: ${CMAKE_SYSTEM_PROCESSOR}")
endif ()

# PROJECT_VERSION
#~ set (PROJECT_VERSION "${Morfeusz_VERSION_MAJOR}.${Morfeusz_VERSION_MINOR}.${Morfeusz_VERSION_PATCH}")

### USER DEFINED VARIABLES

#~ if (CPP_DICTIONARIES_DIR)
    #~ set (INPUT_DICTIONARY_CPP "${CPP_DICTIONARIES_DIR}/${INPUT_DICTIONARY_CPP}")
    #~ set (INPUT_SYNTH_DICTIONARY_CPP "${CPP_DICTIONARIES_DIR}/${INPUT_SYNTH_DICTIONARY_CPP}")
#~ endif ()

if (NOT INPUT_DICTIONARIES)
#   if (EMPTY_INPUT_DICTIONARY)
    set (INPUT_DICTIONARIES ${PROJECT_SOURCE_DIR}/input/empty.txt)
#   else ()
#    set (INPUT_DICTIONARIES "${PROJECT_SOURCE_DIR}/input/sgjp-hom.tab,${PROJECT_SOURCE_DIR}/input/dodatki.tab")
#   endif ()
endif ()

# INPUT_TAGSET
if (NOT INPUT_TAGSET)
   set (INPUT_TAGSET ${PROJECT_SOURCE_DIR}/input/morfeusz-sgjp.tagset)
endif ()

# SEGMENT_RULES_FILE
if (NOT SEGMENT_RULES_FILE)
   set (SEGMENT_RULES_FILE "${PROJECT_SOURCE_DIR}/input/segmenty.dat")
endif ()

message ("Will use ${INPUT_DICTIONARIES} as default dictionary input, ${INPUT_TAGSET} as tagset and ${SEGMENT_RULES_FILE} as segmentation rules")

# TARGET_DIR
if ("${TARGET_DIR}" STREQUAL "")
    set (TARGET_DIR "${PROJECT_BINARY_DIR}")
endif ()

### Compilation and linking flags

if (${CMAKE_SYSTEM_NAME} MATCHES "Linux")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++98 -Wall -pedantic -Wcast-align -Wextra -Wmissing-noreturn -Wconversion -Wcast-qual -Wcast-align -Wno-write-strings")
elseif (${CMAKE_SYSTEM_NAME} MATCHES "Windows" AND CMAKE_CROSSCOMPILING)
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x -Wall -O2")
    set (CMAKE_SHARED_LIBRARY_PREFIX "")
    # here is some magic - must statically link libstdc++ and libgcc
    # but exclude libgcc_eh.a as it causes "multiple definition of (...)" errors
    set (CMAKE_SHARED_LINKER_FLAGS "-s -Os -static-libstdc++ -static-libgcc -Wl,--exclude-libs,libgcc_eh.a")
    set (CMAKE_EXE_LINKER_FLAGS "-s -Os -static-libstdc++ -static-libgcc")
elseif (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++98 -Wall")
    if (NOT INSTALL_NAME_TOOL)
        set (INSTALL_NAME_TOOL install_name_tool)
    endif ()
    #~ set (CMAKE_INSTALL_NAME_DIR @executable_path)
    #~ set (CMAKE_BUILD_WITH_INSTALL_RPATH ON)
    #~ set (MACOSX_RPATH TRUE)
endif ()

########## Configure CPack ##########

# general
set (CPACK_PACKAGE_FILE_NAME "morfeusz2-${Morfeusz_VERSION}-${CMAKE_SYSTEM_NAME}-${ARCHITECTURE}")
set (CPACK_PACKAGE_VENDOR "Michał Lenart")
set (CPACK_PACKAGE_CONTACT "michal.lenart@ipipan.waw.pl")
set (CPACK_DEBIAN_PACKAGE_VERSION "${Morfeusz_VERSION}")
set (CPACK_PACKAGE_DESCRIPTION_SUMMARY "Morphological analyzer for the Polish language.")
set (CPACK_PACKAGE_DESCRIPTION "This is the second version of Morfeusz. Among numerous improvements it has better segmentation and case-sensitive lemmas handling. It also makes it possible to perform morphological synthesis and to use your own dictionary")
set (CPACK_RESOURCE_FILE_LICENSE "${PROJECT_SOURCE_DIR}/License.txt")
set (CPACK_OUTPUT_FILE_PREFIX "${TARGET_DIR}")

if (${CMAKE_SYSTEM_NAME} MATCHES "Linux")
    if (NOT CPACK_GENERATOR)
        set (CPACK_GENERATOR "DEB")
    endif ()
    #debian
    set (CPACK_DEBIAN_PACKAGE_NAME "morfeusz2")
    set (CPACK_DEBIAN_PACKAGE_MAINTAINER "Michał Lenart <${CPACK_PACKAGE_CONTACT}>")
    set (CPACK_DEBIAN_PACKAGE_DEPENDS "libstdc++6 (>= 4.6), libc6")
    set (CPACK_DEBIAN_PACKAGE_ARCHITECTURE "${ARCHITECTURE}")
elseif (${CMAKE_SYSTEM_NAME} MATCHES "Windows" AND NOT CPACK_GENERATOR)
    if (${ARCHITECTURE} MATCHES "amd64")
        set (CPACK_GENERATOR "NSIS64" "TGZ")
    else ()
        set (CPACK_GENERATOR "NSIS" "TGZ")
    endif ()
elseif (${CMAKE_SYSTEM_NAME} MATCHES "Darwin" AND NOT CPACK_GENERATOR)
    set (CPACK_GENERATOR "TGZ")
endif ()

include (CPack)

##### END initialize some vars #####
file (COPY fsabuilder doTest.sh testJavaWrapper.sh testPythonWrapper.sh morfeusz/wrappers/python/test.py DESTINATION .)

###### add main sources ########

add_subdirectory (morfeusz)
add_subdirectory (fsabuilder)

########## add tests ##########

macro (test_analyzer analyzerDir)
#    message ("adding test dir ${analyzerDir}")
    get_filename_component (dirname ${analyzerTestDir} NAME)
    add_test(TestAnalyzer_${dirname} ./doTest.sh morfeusz analyzer ${analyzerDir})
endmacro()

macro (test_generator generatorDir)
#    message ("adding test dir ${generatorDir}")
    get_filename_component (dirname ${generatorTestDir} NAME)
    add_test(TestGenerator_${dirname} ./doTest.sh morfeusz generator ${generatorDir})
endmacro()

file (GLOB analyzerTestDirs "tests/analyzer/*")
if (UNIX)
    foreach (analyzerTestDir ${analyzerTestDirs})
        test_analyzer(${analyzerTestDir})
    endforeach()
endif()

file (GLOB generatorTestDirs "tests/generator/*")
if (UNIX)
    foreach (generatorTestDir ${generatorTestDirs})
        test_generator(${generatorTestDir})
    endforeach()
endif()

if (UNIX AND EMBEDDED_DEFAULT_DICT)
    add_test(TestJavaWrapper ./testJavaWrapper.sh "${CMAKE_CURRENT_SOURCE_DIR}" "${PROJECT_BINARY_DIR}")
    add_test(TestPythonWrapper ./testPythonWrapper.sh "${PROJECT_BINARY_DIR}")
else ()
    message(WARNING "Will skip Java and Python wrapper tests - must be on UNIX and with EMBEDDED_DEFAULT_DICT on to run them")
endif ()
