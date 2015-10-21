/*==============================================================================

  Program: 3D Slicer

  Portions (c) Copyright Brigham and Women's Hospital (BWH) All Rights Reserved.

  See COPYRIGHT.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

==============================================================================*/

// .NAME vtkSlicerPointSetProcessingCppLogic - slicer logic class for volumes manipulation
// .SECTION Description
// This class manages the logic associated with reading, saving,
// and changing propertied of the volumes


#ifndef __vtkSlicerPointSetProcessingCppLogic_h
#define __vtkSlicerPointSetProcessingCppLogic_h

// Slicer includes
#include "vtkSlicerModuleLogic.h"

// MRML includes

// STD includes
#include <cstdlib>

#include "vtkSlicerPointSetProcessingCppModuleLogicExport.h"

class vtkMRMLModelNode;
class vtkPolyData;

/// \ingroup Slicer_QtModules_ExtensionTemplate
class VTK_SLICER_POINTSETPROCESSINGCPP_MODULE_LOGIC_EXPORT vtkSlicerPointSetProcessingCppLogic :
  public vtkSlicerModuleLogic
{
public:

  static vtkSlicerPointSetProcessingCppLogic *New();
  vtkTypeMacro(vtkSlicerPointSetProcessingCppLogic, vtkSlicerModuleLogic);
  void PrintSelf(ostream& os, vtkIndent indent);

  float Apply_vtkPointSetOutlierRemoval(vtkMRMLModelNode* input, double percentToRemove = 0.01, bool verbose = false);

  float Apply_vtkPointSetNormalEstimation(vtkMRMLModelNode* input, vtkMRMLModelNode* output, vtkMRMLModelNode* orientatedGlyphs, unsigned int mode = 1, unsigned int numberOfNeighbors = 4, float radius = 1.0, int kNearestNeighbors = 5, unsigned int graphType = 1, bool addGlyphs = false, bool verbose = false);
  float Apply_vtkPolyDataNormals(vtkMRMLModelNode* input, vtkMRMLModelNode* output, vtkMRMLModelNode* orientatedGlyphs, double featureAngle = 0.1, bool splitting = true, bool consistency = false, bool autoOrientNormals = false, bool computePointNormals = true, bool computeCellNormals = false, bool flipNormals = false, bool nonManifoldTraversal = true, bool addGlyphs = false, bool verbose = false);
  
  float Apply_vtkPoissionReconstruction(vtkMRMLModelNode* input, vtkMRMLModelNode* output, int depth = 8, float scale = 1.25, int solverDivide = 8, int isoDivide = 8, float samplesPerNode = 1.0, int confidence = 0, int verboseAlgorithm = 0, bool verbose = false);
  float Apply_vtkDelaunay3D(vtkMRMLModelNode* input, vtkMRMLModelNode* output, double alpha = 0.0, double tolerance = 0.0, double offset = 2.5, bool boudingTriangulation = false, bool verbose = false);
  
protected:
  vtkSlicerPointSetProcessingCppLogic();
  virtual ~vtkSlicerPointSetProcessingCppLogic();

  virtual void SetMRMLSceneInternal(vtkMRMLScene* newScene);
  /// Register MRML Node classes to Scene. Gets called automatically when the MRMLScene is attached to this logic class.
  virtual void RegisterNodes();
  virtual void UpdateFromMRMLScene();
  virtual void OnMRMLSceneNodeAdded(vtkMRMLNode* node);
  virtual void OnMRMLSceneNodeRemoved(vtkMRMLNode* node);
private:

  bool HasPointNormals(vtkMRMLModelNode* input, bool verbose = false);
  bool HasCellNormals(vtkMRMLModelNode* input, bool verbose = false);
  bool HasPoints(vtkMRMLModelNode* input, bool verbose = false);
  void OutputGlyphs3D(vtkPolyData* inputPolyData, vtkMRMLModelNode* ouputModelNode, double scaleFactor = 4.0, double tolerance = 0.1);

  vtkSlicerPointSetProcessingCppLogic(const vtkSlicerPointSetProcessingCppLogic&); // Not implemented
  void operator=(const vtkSlicerPointSetProcessingCppLogic&); // Not implemented
};

#endif
