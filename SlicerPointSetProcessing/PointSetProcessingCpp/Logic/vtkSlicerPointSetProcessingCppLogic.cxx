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

// PointSetProcessingCpp Logic includes
#include "vtkSlicerPointSetProcessingCppLogic.h"

// MRML includes
#include <vtkMRMLModelNode.h>
#include <vtkMRMLScene.h>

// VTK includes
#include <vtkArrowSource.h>
#include <vtkCellData.h>
#include <vtkCleanPolyData.h>
#include <vtkDelaunay3D.h>
#include <vtkDoubleArray.h>
#include <vtkFloatArray.h>
#include <vtkGeometryFilter.h>
#include <vtkGlyph3D.h>
#include <vtkIntArray.h>
#include <vtkNew.h>
#include <vtkObjectFactory.h>
#include <vtkPointData.h>
#include <vtkPolyDataNormals.h>
#include <vtkTimerLog.h>

// STD includes
#include <cassert>
#include <exception> 

#include <vtkPointSetNormalEstimation.h>
#include <vtkPointSetNormalOrientation.h>
#include <vtkPointSetOutlierRemoval.h>
#include <vtkPoissonReconstruction.h>

//----------------------------------------------------------------------------
vtkStandardNewMacro(vtkSlicerPointSetProcessingCppLogic);

//----------------------------------------------------------------------------
vtkSlicerPointSetProcessingCppLogic::vtkSlicerPointSetProcessingCppLogic()
{
}

//----------------------------------------------------------------------------
vtkSlicerPointSetProcessingCppLogic::~vtkSlicerPointSetProcessingCppLogic()
{
}

//----------------------------------------------------------------------------
void vtkSlicerPointSetProcessingCppLogic::PrintSelf(ostream& os, vtkIndent indent)
{
  this->Superclass::PrintSelf(os, indent);
}

//---------------------------------------------------------------------------
void vtkSlicerPointSetProcessingCppLogic::SetMRMLSceneInternal(vtkMRMLScene * newScene)
{
  vtkNew<vtkIntArray> events;
  events->InsertNextValue(vtkMRMLScene::NodeAddedEvent);
  events->InsertNextValue(vtkMRMLScene::NodeRemovedEvent);
  events->InsertNextValue(vtkMRMLScene::EndBatchProcessEvent);
  this->SetAndObserveMRMLSceneEventsInternal(newScene, events.GetPointer());
}

//-----------------------------------------------------------------------------
void vtkSlicerPointSetProcessingCppLogic::RegisterNodes()
{
  assert(this->GetMRMLScene() != 0);
}

//---------------------------------------------------------------------------
void vtkSlicerPointSetProcessingCppLogic::UpdateFromMRMLScene()
{
  assert(this->GetMRMLScene() != 0);
}

//---------------------------------------------------------------------------
void vtkSlicerPointSetProcessingCppLogic
::OnMRMLSceneNodeAdded(vtkMRMLNode* vtkNotUsed(node))
{
}

//---------------------------------------------------------------------------
void vtkSlicerPointSetProcessingCppLogic
::OnMRMLSceneNodeRemoved(vtkMRMLNode* vtkNotUsed(node))
{
}

//---------------------------------------------------------------------------
float vtkSlicerPointSetProcessingCppLogic
::Apply_vtkPointSetOutlierRemoval(vtkMRMLModelNode* input, double percentToRemove, bool verbose)
{
  vtkInfoMacro("vtkSlicerPointSetProcessingCppLogic::Apply_vtkPointSetOutlierRemoval");

  if (verbose)
  {
    std::cout << "Apply_vtkPointSetOutlierRemoval(verbose = " << verbose << "percentToRemove = " << percentToRemove << ")" << std::endl;
  }

  if (this->HasPoints(input, verbose))
  {
    vtkSmartPointer<vtkTimerLog> timer = vtkSmartPointer<vtkTimerLog>::New();
    timer->StartTimer();
	
    vtkSmartPointer<vtkPointSetOutlierRemoval> outlierRemoval = vtkSmartPointer<vtkPointSetOutlierRemoval>::New();
    outlierRemoval->SetInputConnection(input->GetPolyDataConnection());
    outlierRemoval->SetPercentToRemove(percentToRemove); //remove percentToRemove of the points
    outlierRemoval->Update();

    input->SetAndObservePolyData(outlierRemoval->GetOutput());
         
    timer->StopTimer();
    float runtime = timer->GetElapsedTime();
    return runtime;
  }
  vtkWarningMacro("Point data in vtkPolyData contains no points!");
  return 0;
}

//---------------------------------------------------------------------------
float vtkSlicerPointSetProcessingCppLogic
::Apply_vtkPointSetNormalEstimation(vtkMRMLModelNode* input, vtkMRMLModelNode* output, vtkMRMLModelNode* orientatedGlyphs, unsigned int mode, unsigned int numberOfNeighbors, float radius, int kNearestNeighbors, unsigned int graphType, bool addGlyphs, bool verbose)
{
  vtkInfoMacro("vtkSlicerPointSetProcessingCppLogic::Apply_vtkPointSetNormalEstimation");

  if (verbose)
  {
    std::cout << "Apply_vtkPointSetNormalEstimation(mode = " << mode << ", numberOfNeighbors = " << numberOfNeighbors << ", radius = " << radius << ", kNearestNeighbors = " << kNearestNeighbors << ", graphType = " << graphType << ", addGlyphs = " << addGlyphs << ", verbose = " << verbose << ")" << std::endl;
  }

  if (this->HasPoints(input, verbose))
  {
    vtkSmartPointer<vtkTimerLog> timer = vtkSmartPointer<vtkTimerLog>::New();
    timer->StartTimer();
	
    // vtkPointSetNormalEstimation
    vtkSmartPointer<vtkPointSetNormalEstimation> normalEstimation = vtkSmartPointer<vtkPointSetNormalEstimation>::New();
    normalEstimation->SetInputConnection(input->GetPolyDataConnection());
    if (mode == vtkPointSetNormalEstimation::FIXED_NUMBER)
    {
      normalEstimation->SetModeToFixedNumber();
      normalEstimation->SetNumberOfNeighbors(numberOfNeighbors);
    }
    else if (mode == vtkPointSetNormalEstimation::RADIUS)
    {
      normalEstimation->SetModeToRadius();
      normalEstimation->SetRadius(radius);
    }
    else
    {
      vtkWarningMacro("Invalid mode! Should be either 0 (FIXED_NUMBER) or 1 (RADIUS).");
      return 0;
    }

    // vtkPointSetNormalOrientation
    vtkSmartPointer<vtkPointSetNormalOrientation> normalOrientationFilter = vtkSmartPointer<vtkPointSetNormalOrientation>::New();
    normalOrientationFilter->SetInputConnection(normalEstimation->GetOutputPort()); 
    if (graphType == vtkPointSetNormalOrientation::KNN_GRAPH)
    {
      normalOrientationFilter->SetGraphFilterType(vtkPointSetNormalOrientation::KNN_GRAPH);
      normalOrientationFilter->SetKNearestNeighbors(kNearestNeighbors);
    }
    else if (graphType == vtkPointSetNormalOrientation::RIEMANN_GRAPH)
    {
      normalOrientationFilter->SetGraphFilterType(vtkPointSetNormalOrientation::RIEMANN_GRAPH);
    }
    else
    {
      vtkWarningMacro("Invalid graphType! Should be either 0 (RIEMANN_GRAPH) or 1 (KNN_GRAPH).");
      return 0;
    }

    try
    {
      normalOrientationFilter->Update();	
    }
    catch(std::exception const&  ex)
    {
      vtkWarningMacro("Could not execute vtkPointSetNormalOrientation: " << ex.what());
      return 0;
    }        

    output->SetAndObservePolyData(normalOrientationFilter->GetOutput());

    if (addGlyphs)
    {
      OutputGlyphs3D(normalOrientationFilter->GetOutput(), orientatedGlyphs);
    }
         
    timer->StopTimer();
    float runtime = timer->GetElapsedTime();
    return runtime;
  }
  vtkWarningMacro("Point data in vtkPolyData contains no points!");
  return 0;
}

//---------------------------------------------------------------------------
float vtkSlicerPointSetProcessingCppLogic
::Apply_vtkPolyDataNormals(vtkMRMLModelNode* input, vtkMRMLModelNode* output, vtkMRMLModelNode* orientatedGlyphs, double featureAngle, bool splitting, bool consistency, bool autoOrientNormals, bool computePointNormals, bool computeCellNormals, bool flipNormals, bool nonManifoldTraversal, bool addGlyphs, bool verbose)
{
  vtkInfoMacro("vtkSlicerPointSetProcessingCppLogic::Apply_vtkPolyDataNormals");

  if (verbose)
  {
    std::cout << "Apply_vtkPolyDataNormals(featureAngle = " << featureAngle << ", splitting = " << splitting << ", consistency = " << consistency << ", autoOrientNormals = " << autoOrientNormals << ", computePointNormals = " << computePointNormals << ", computeCellNormals = " << computeCellNormals << ", flipNormals = " << flipNormals << ", nonManifoldTraversal = " << nonManifoldTraversal << ", addGlyphs = " << addGlyphs << ", verbose = " << verbose << ")" << std::endl;
  }

  if (this->HasPoints(input, verbose))
  {
    vtkSmartPointer<vtkTimerLog> timer = vtkSmartPointer<vtkTimerLog>::New();
    timer->StartTimer();
	
    vtkSmartPointer<vtkPolyDataNormals> polyDataNormals = vtkSmartPointer<vtkPolyDataNormals>::New();
    polyDataNormals->SetInputConnection(input->GetPolyDataConnection());
    polyDataNormals->SetFeatureAngle(featureAngle);
    polyDataNormals->SetSplitting(splitting); 
    polyDataNormals->SetConsistency(consistency);
    polyDataNormals->SetAutoOrientNormals(autoOrientNormals);
    polyDataNormals->SetComputePointNormals(computePointNormals);
    polyDataNormals->SetComputeCellNormals(computeCellNormals);
    polyDataNormals->SetFlipNormals(flipNormals);
    polyDataNormals->SetNonManifoldTraversal(nonManifoldTraversal);
    polyDataNormals->Update();	

    output->SetAndObservePolyData(polyDataNormals->GetOutput());

    if (addGlyphs)
    {
      OutputGlyphs3D(polyDataNormals->GetOutput(), orientatedGlyphs);
    }
    
    timer->StopTimer();
    float runtime = timer->GetElapsedTime();
    return runtime;
  }
  vtkWarningMacro("Point data in vtkPolyData contains no points!");
  return 0;
}

//---------------------------------------------------------------------------
float vtkSlicerPointSetProcessingCppLogic
::Apply_vtkPoissionReconstruction(vtkMRMLModelNode* input, vtkMRMLModelNode* output, int depth, float scale, int solverDivide, int isoDivide, float samplesPerNode, int confidence, int verboseAlgorithm, bool verbose)
{
  vtkInfoMacro("vtkSlicerPointSetProcessingCppLogic::Apply_vtkPoissionReconstruction");

  if (verbose)
  {
    std::cout << "Apply_vtkPoissionReconstruction(depth = " << depth << ", scale = " << scale << ", solverDivide = " << solverDivide << ", isoDivide = " << isoDivide << ", samplesPerNode = " << samplesPerNode << ", confidence = " << confidence << ", verboseAlgorithm =" << verboseAlgorithm << ", verbose =" << verbose << ")" << std::endl;
  }

  if (this->HasPointNormals(input, verbose))
  {
    vtkSmartPointer<vtkTimerLog> timer = vtkSmartPointer<vtkTimerLog>::New();
    timer->StartTimer();

    // vtkPoissonReconstruction
    vtkSmartPointer<vtkPoissonReconstruction> poissonFilter = vtkSmartPointer<vtkPoissonReconstruction>::New();
    poissonFilter->SetInputConnection(input->GetPolyDataConnection());
    poissonFilter->SetDepth(depth);
    poissonFilter->SetScale(scale);
    poissonFilter->SetSolverDivide(solverDivide); 
    poissonFilter->SetIsoDivide(isoDivide); 
    poissonFilter->SetSamplesPerNode(samplesPerNode);
    poissonFilter->SetConfidence(confidence); 
    poissonFilter->SetVerbose(verboseAlgorithm);   
    poissonFilter->Update();	

    output->SetAndObservePolyData(poissonFilter->GetOutput());

    timer->StopTimer();
    float runtime = timer->GetElapsedTime();
    return runtime;
  }
  vtkWarningMacro("Point data in vtkPolyData contains no point normals!");
  return 0;
}

//---------------------------------------------------------------------------
float vtkSlicerPointSetProcessingCppLogic
::Apply_vtkDelaunay3D(vtkMRMLModelNode* input, vtkMRMLModelNode* output, double alpha, double tolerance, double offset, bool boudingTriangulation, bool verbose)
{
  vtkInfoMacro("vtkSlicerPointSetProcessingCppLogic::Apply_vtkDelaunay3D");

  if (verbose)
  {
    std::cout << "Apply_vtkDelaunay3D(alpha = " << alpha << ", tolerance = " << tolerance << ", offset = " << offset << ", boudingTriangulation = " << boudingTriangulation << ")" << std::endl;
  }

  if (this->HasPoints(input, verbose)) // Normals not necessary here?
  {
    vtkSmartPointer<vtkTimerLog> timer = vtkSmartPointer<vtkTimerLog>::New();
    timer->StartTimer();

    vtkSmartPointer<vtkDelaunay3D> delaunay3D = vtkSmartPointer<vtkDelaunay3D>::New();
    delaunay3D->SetInputConnection(input->GetPolyDataConnection());
    delaunay3D->SetAlpha(alpha); 
    delaunay3D->SetTolerance(tolerance);
    delaunay3D->SetOffset(offset);
    delaunay3D->SetBoundingTriangulation(boudingTriangulation);

    vtkSmartPointer<vtkGeometryFilter> geometryFilter = vtkSmartPointer<vtkGeometryFilter>::New();
    geometryFilter->SetInputConnection(delaunay3D->GetOutputPort());
    geometryFilter->Update(); 

    output->SetAndObservePolyData(geometryFilter->GetOutput());
      
    timer->StopTimer();
    float runtime = timer->GetElapsedTime();
    return runtime;
  }
  vtkWarningMacro("Point data in vtkPolyData contains no points!");
  return 0;
}

//---------------------------------------------------------------------------
bool vtkSlicerPointSetProcessingCppLogic
::HasPointNormals(vtkMRMLModelNode* input, bool verbose)
{
  vtkInfoMacro("vtkSlicerPointSetProcessingCppLogic::HasPointNormals");

  if (HasPoints(input, verbose))
  {
	  vtkPolyData* polydata = input->GetPolyData();

    if (verbose)
    {
      std::cout << "Looking for point normals..." << std::endl;
   
      // Count points
      vtkIdType numPoints = polydata->GetNumberOfPoints();
      std::cout << "There are " << numPoints << " points." << std::endl;
   
      // Count triangles
      vtkIdType numPolys = polydata->GetNumberOfPolys();
      std::cout << "There are " << numPolys << " polys." << std::endl;
    }

    ////////////////////////////////////////////////////////////////
    // Double normals in an array
    vtkDoubleArray* normalDataDouble = vtkDoubleArray::SafeDownCast(polydata->GetPointData()->GetArray("Normals"));
   
    if(normalDataDouble)
    {
      int nc = normalDataDouble->GetNumberOfTuples();
      if (verbose)
      {
        std::cout << "There are " << nc << " components in normalDataDouble" << std::endl;
      }
      return true;
    }
   
    ////////////////////////////////////////////////////////////////
    // Double normals in an array
    vtkFloatArray* normalDataFloat = vtkFloatArray::SafeDownCast(polydata->GetPointData()->GetArray("Normals"));
   
    if(normalDataFloat)
    {
      int nc = normalDataFloat->GetNumberOfTuples();
      if (verbose)
      {
        std::cout << "There are " << nc << " components in normalDataFloat" << std::endl;
      }
      return true;
    }
   
    ////////////////////////////////////////////////////////////////
    // Point normals
    vtkDoubleArray* normalsDouble = vtkDoubleArray::SafeDownCast(polydata->GetPointData()->GetNormals());
   
    if(normalsDouble)
    {
      if (verbose)
      {
        std::cout << "There are " << normalsDouble->GetNumberOfComponents() << " components in normalsDouble" << std::endl;
      }
      return true;
    }
   
    ////////////////////////////////////////////////////////////////
    // Point normals
    vtkFloatArray* normalsFloat = vtkFloatArray::SafeDownCast(polydata->GetPointData()->GetNormals());
   
    if(normalsFloat)
    {
      if (verbose)
      {
        std::cout << "There are " << normalsFloat->GetNumberOfComponents() << " components in normalsFloat" << std::endl;
      }
      return true;
    }
   
    /////////////////////////////////////////////////////////////////////
    // Generic type point normals
    vtkDataArray* normalsGeneric = polydata->GetPointData()->GetNormals(); 
    if(normalsGeneric)
    {
      if (verbose)
      {
        std::cout << "There are " << normalsGeneric->GetNumberOfTuples() << " normals in normalsGeneric" << std::endl;
      }
   
      double testDouble[3];
      normalsGeneric->GetTuple(0, testDouble);
   
      if (verbose)
      {
        std::cout << "Double: " << testDouble[0] << " " << testDouble[1] << " " << testDouble[2] << std::endl;
      }
      return true;
    }     
  }
  // If the function has not yet quit, there were none of these types of normals
  if (verbose)
  {
    std::cout << "Normals not found!" << std::endl;
  }
  return false;  
}

//---------------------------------------------------------------------------
bool vtkSlicerPointSetProcessingCppLogic
::HasCellNormals(vtkMRMLModelNode* input, bool verbose)
{
  vtkInfoMacro("vtkSlicerPointSetProcessingCppLogic::HasCellNormals");

  if (HasPoints(input, verbose))
  {
	  vtkPolyData* polydata = input->GetPolyData();

    if (verbose)
    {
      std::cout << "Looking for cell normals..." << std::endl;
   
      // Count points
      vtkIdType numCells = polydata->GetNumberOfCells();
      std::cout << "There are " << numCells << " cells." << std::endl;
   
      // Count triangles
      vtkIdType numPolys = polydata->GetNumberOfPolys();
      std::cout << "There are " << numPolys << " polys." << std::endl;
    }

    ////////////////////////////////////////////////////////////////
    // Double normals in an array
    vtkDoubleArray* normalDataDouble = vtkDoubleArray::SafeDownCast(polydata->GetCellData()->GetArray("Normals"));
   
    if(normalDataDouble)
    {
      int nc = normalDataDouble->GetNumberOfTuples();
      if (verbose)
      {
        std::cout << "There are " << nc << " components in normalDataDouble" << std::endl;
      }
      return true;
    }
   
    ////////////////////////////////////////////////////////////////
    // Double normals in an array
    vtkFloatArray* normalDataFloat = vtkFloatArray::SafeDownCast(polydata->GetCellData()->GetArray("Normals"));
   
    if(normalDataFloat)
    {
      int nc = normalDataFloat->GetNumberOfTuples();
      if (verbose)
      {
        std::cout << "There are " << nc << " components in normalDataFloat" << std::endl;
      }
      return true;
    }
   
    ////////////////////////////////////////////////////////////////
    // Point normals
    vtkDoubleArray* normalsDouble = vtkDoubleArray::SafeDownCast(polydata->GetCellData()->GetNormals());
   
    if(normalsDouble)
    {
      if (verbose)
      {
        std::cout << "There are " << normalsDouble->GetNumberOfComponents() << " components in normalsDouble" << std::endl;
      }
      return true;
    }
   
    ////////////////////////////////////////////////////////////////
    // Point normals
    vtkFloatArray* normalsFloat = vtkFloatArray::SafeDownCast(polydata->GetCellData()->GetNormals());
   
    if(normalsFloat)
    {
      if (verbose)
      {
        std::cout << "There are " << normalsFloat->GetNumberOfComponents() << " components in normalsFloat" << std::endl;
      }
      return true;
    }
   
    /////////////////////////////////////////////////////////////////////
    // Generic type point normals
    vtkDataArray* normalsGeneric = polydata->GetCellData()->GetNormals();
    if(normalsGeneric)
    {
      if (verbose)
      {
        std::cout << "There are " << normalsGeneric->GetNumberOfTuples() << " normals in normalsGeneric" << std::endl;
      } 
      double testDouble[3];
      normalsGeneric->GetTuple(0, testDouble);
      
      if (verbose)
      { 
        std::cout << "Double: " << testDouble[0] << " " << testDouble[1] << " " << testDouble[2] << std::endl;
      }
      return true;
    }
  }
  // If the function has not yet quit, there were none of these types of normals
  if (verbose)
  {
    std::cout << "Normals not found!" << std::endl;
  }
  return false;
}

bool vtkSlicerPointSetProcessingCppLogic
::HasPoints(vtkMRMLModelNode* input, bool verbose)
{
  vtkInfoMacro("vtkSlicerPointSetProcessingCppLogic::HasPoints");

  if (input != NULL)
  {
	  vtkPolyData* polydata = input->GetPolyData();
    if (polydata != NULL)
    {
      if (verbose)
      {
        std::cout << "vtkPolyData contains " << polydata->GetNumberOfPoints() << " points" << std::endl;
      }

      if (polydata->GetNumberOfPoints() > 0)
      {
        return true;
      }
    }
  }
  return false;
}

//---------------------------------------------------------------------------
void vtkSlicerPointSetProcessingCppLogic
::OutputGlyphs3D(vtkPolyData* inputPolyData, vtkMRMLModelNode* ouputModelNode, double scaleFactor, double tolerance)
{
  vtkSmartPointer<vtkCleanPolyData> cleanPolyData = vtkSmartPointer<vtkCleanPolyData>::New();
  cleanPolyData->SetInputData(inputPolyData);
  cleanPolyData->SetTolerance(tolerance);
  cleanPolyData->Update();

  vtkSmartPointer<vtkGlyph3D> glyph3D = vtkSmartPointer<vtkGlyph3D>::New();
  glyph3D->SetInputData(cleanPolyData->GetOutput());

  vtkSmartPointer<vtkArrowSource> arrowSource  = vtkSmartPointer<vtkArrowSource>::New();
  glyph3D->SetSourceConnection(arrowSource->GetOutputPort());
  glyph3D->SetVectorModeToUseNormal();
  glyph3D->SetScaleFactor(scaleFactor);  
  glyph3D->Update();
  
  ouputModelNode->SetAndObservePolyData(glyph3D->GetOutput());  
}