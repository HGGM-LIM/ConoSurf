project(vtkSlicer${MODULE_NAME}ModuleLogic)

set(KIT ${PROJECT_NAME})

set(${KIT}_EXPORT_DIRECTIVE "VTK_SLICER_${MODULE_NAME_UPPER}_MODULE_LOGIC_EXPORT")

# Future super-build here
# Fork and build from my GitHub

# PointSetProcessing
find_library(POINTSETPROCESSING_LIBRARY PointSetProcessing
          PATHS "H:/_B/VTK-filters/PointSetProcessingR/Release"
          DOC "Path to the PointSetProcessing library." )  
find_path(POINTSETPROCESSING_INCLUDE_DIR vtkPointSetNormalEstimation.h
          PATHS "H:/_S/VTK-filters/PointSetProcessing"
          DOC "Path to PointSetProcessing include directory." )                        

# PoissonReconstruction
find_path(POISSONRECONSTRUCTION_BUILD_DIR vtkPoissonReconstructionConfigure.h
          PATHS "H:/_B/VTK-filters/PoissonReconstructionR"
          DOC "Path to PoissonReconstruction build directory." )
find_path(POISSONRECONSTRUCTION_INCLUDE_DIR vtkPoissonReconstruction.h
          PATHS "H:/_S/VTK-filters/PoissonReconstruction/source"
          DOC "Path to PoissonReconstruction include directory." )
find_library(POISSONRECONSTRUCTION_LIBRARY vtkPoissonReconstruction
          PATHS "H:/_B/VTK-filters/PoissonReconstructionR/lib/Release"
          DOC "Path to the PoissonReconstruction library." )
          
# vtkInfovisBoostGraphAlgorithms
find_library(INFOVISBOOSTGRAPH_ALGORITHMS vtkInfovisBoostGraphAlgorithms-6.3
          PATHS "H:/_B/S4R/VTKv6-build/lib/Release"
          DOC "Path to the vtkInfovisBoostGraphAlgorithms-6.3 library." )
           
if (NOT POINTSETPROCESSING_LIBRARY)
  message( FATAL_ERROR "PointSetProcessing library not found." )
elseif (NOT POINTSETPROCESSING_INCLUDE_DIR)
  message( FATAL_ERROR "PointSetProcessing include directory not found." )          
elseif (NOT POISSONRECONSTRUCTION_LIBRARY)
  message( FATAL_ERROR "PoissonReconstruction library not found." )
elseif (NOT POISSONRECONSTRUCTION_BUILD_DIR)
  message( FATAL_ERROR "PoissonReconstruction build directory not found." )
elseif (NOT POISSONRECONSTRUCTION_INCLUDE_DIR)
  message( FATAL_ERROR "PoissonReconstruction include directory not found." )
elseif (NOT INFOVISBOOSTGRAPH_ALGORITHMS)
  message( FATAL_ERROR "vtkInfovisBoostGraphAlgorithms-6.3 library not found." )
endif()

set(${KIT}_INCLUDE_DIRECTORIES
  "${POINTSETPROCESSING_INCLUDE_DIR}"
  "${POISSONRECONSTRUCTION_INCLUDE_DIR}"
  "${POISSONRECONSTRUCTION_BUILD_DIR}"
  )

set(${KIT}_SRCS
  vtkSlicer${MODULE_NAME}Logic.cxx
  vtkSlicer${MODULE_NAME}Logic.h
  )

set(${KIT}_TARGET_LIBRARIES
  "${POINTSETPROCESSING_LIBRARY}"
  "${POISSONRECONSTRUCTION_LIBRARY}"
  "${INFOVISBOOSTGRAPH_ALGORITHMS}"
  )

#-----------------------------------------------------------------------------
SlicerMacroBuildModuleLogic(
  NAME ${KIT}
  EXPORT_DIRECTIVE ${${KIT}_EXPORT_DIRECTIVE}
  INCLUDE_DIRECTORIES ${${KIT}_INCLUDE_DIRECTORIES}
  SRCS ${${KIT}_SRCS}
  TARGET_LIBRARIES ${${KIT}_TARGET_LIBRARIES}
  )
