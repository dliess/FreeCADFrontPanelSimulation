add_library(FpSimGrpc STATIC IMPORTED)
find_library(FPSIMGRPC_LIBRARY_PATH  FpSimGrpc HINTS "~/.FreeCAD/Mod/FreeCADFrontPanelSimulation/generated/c++")
set_target_properties(FpSimGrpc PROPERTIES IMPORTED_LOCATION "${FPSIMGRPC_LIBRARY_PATH}")
