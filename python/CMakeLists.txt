
find_program (PYTHON_BIN "python")

if (PYTHON_BIN)
    set (SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in")
    set (SETUP_PY "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
    set (PYTHON_LIB_NAME "Sim.so")

    get_filename_component (SIM_SOURCE Sim.cpp ABSOLUTE)
    
    configure_file (${SETUP_PY_IN} ${SETUP_PY})
    add_custom_target (PythonLib ALL ${PYTHON_BIN} ${SETUP_PY} build SOURCES ${SIM_SOURCE})
    add_dependencies (PythonLib ${CUSHION_LIB_NAME})
endif (PYTHON_BIN)

