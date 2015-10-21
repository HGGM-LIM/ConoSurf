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

// Qt includes
#include <QtPlugin>

// PointSetProcessingCpp Logic includes
#include <vtkSlicerPointSetProcessingCppLogic.h>

// PointSetProcessingCpp includes
#include "qSlicerPointSetProcessingCppModule.h"
#include "qSlicerPointSetProcessingCppModuleWidget.h"

//-----------------------------------------------------------------------------
Q_EXPORT_PLUGIN2(qSlicerPointSetProcessingCppModule, qSlicerPointSetProcessingCppModule);

//-----------------------------------------------------------------------------
/// \ingroup Slicer_QtModules_ExtensionTemplate
class qSlicerPointSetProcessingCppModulePrivate
{
public:
  qSlicerPointSetProcessingCppModulePrivate();
};

//-----------------------------------------------------------------------------
// qSlicerPointSetProcessingCppModulePrivate methods

//-----------------------------------------------------------------------------
qSlicerPointSetProcessingCppModulePrivate::qSlicerPointSetProcessingCppModulePrivate()
{
}

//-----------------------------------------------------------------------------
// qSlicerPointSetProcessingCppModule methods

//-----------------------------------------------------------------------------
qSlicerPointSetProcessingCppModule::qSlicerPointSetProcessingCppModule(QObject* _parent)
  : Superclass(_parent)
  , d_ptr(new qSlicerPointSetProcessingCppModulePrivate)
{
}

//-----------------------------------------------------------------------------
qSlicerPointSetProcessingCppModule::~qSlicerPointSetProcessingCppModule()
{
}

//-----------------------------------------------------------------------------
QString qSlicerPointSetProcessingCppModule::helpText() const
{
  return "This is a loadable module that can be bundled in an extension";
}

//-----------------------------------------------------------------------------
QString qSlicerPointSetProcessingCppModule::acknowledgementText() const
{
  return "This work was partially funded by NIH grant NXNNXXNNNNNN-NNXN";
}

//-----------------------------------------------------------------------------
QStringList qSlicerPointSetProcessingCppModule::contributors() const
{
  QStringList moduleContributors;
  moduleContributors << QString("Mikael Brudfors (CMIC, UCL, London, UK)");
  return moduleContributors;
}

//-----------------------------------------------------------------------------
QIcon qSlicerPointSetProcessingCppModule::icon() const
{
  return QIcon(":/Icons/PointSetProcessingCpp.png");
}

//-----------------------------------------------------------------------------
QStringList qSlicerPointSetProcessingCppModule::categories() const
{
  return QStringList() << "Examples";
}

//-----------------------------------------------------------------------------
QStringList qSlicerPointSetProcessingCppModule::dependencies() const
{
  return QStringList();
}

//-----------------------------------------------------------------------------
void qSlicerPointSetProcessingCppModule::setup()
{
  this->Superclass::setup();
}

//-----------------------------------------------------------------------------
qSlicerAbstractModuleRepresentation* qSlicerPointSetProcessingCppModule
::createWidgetRepresentation()
{
  return new qSlicerPointSetProcessingCppModuleWidget;
}

//-----------------------------------------------------------------------------
vtkMRMLAbstractLogic* qSlicerPointSetProcessingCppModule::createLogic()
{
  return vtkSlicerPointSetProcessingCppLogic::New();
}
