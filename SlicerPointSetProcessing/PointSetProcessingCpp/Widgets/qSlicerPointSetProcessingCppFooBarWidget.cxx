/*==============================================================================

  Program: 3D Slicer

  Copyright (c) Kitware Inc.

  See COPYRIGHT.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
  and was partially funded by NIH grant 3P41RR013218-12S1

==============================================================================*/

// FooBar Widgets includes
#include "qSlicerPointSetProcessingCppFooBarWidget.h"
#include "ui_qSlicerPointSetProcessingCppFooBarWidget.h"

//-----------------------------------------------------------------------------
/// \ingroup Slicer_QtModules_PointSetProcessingCpp
class qSlicerPointSetProcessingCppFooBarWidgetPrivate
  : public Ui_qSlicerPointSetProcessingCppFooBarWidget
{
  Q_DECLARE_PUBLIC(qSlicerPointSetProcessingCppFooBarWidget);
protected:
  qSlicerPointSetProcessingCppFooBarWidget* const q_ptr;

public:
  qSlicerPointSetProcessingCppFooBarWidgetPrivate(
    qSlicerPointSetProcessingCppFooBarWidget& object);
  virtual void setupUi(qSlicerPointSetProcessingCppFooBarWidget*);
};

// --------------------------------------------------------------------------
qSlicerPointSetProcessingCppFooBarWidgetPrivate
::qSlicerPointSetProcessingCppFooBarWidgetPrivate(
  qSlicerPointSetProcessingCppFooBarWidget& object)
  : q_ptr(&object)
{
}

// --------------------------------------------------------------------------
void qSlicerPointSetProcessingCppFooBarWidgetPrivate
::setupUi(qSlicerPointSetProcessingCppFooBarWidget* widget)
{
  this->Ui_qSlicerPointSetProcessingCppFooBarWidget::setupUi(widget);
}

//-----------------------------------------------------------------------------
// qSlicerPointSetProcessingCppFooBarWidget methods

//-----------------------------------------------------------------------------
qSlicerPointSetProcessingCppFooBarWidget
::qSlicerPointSetProcessingCppFooBarWidget(QWidget* parentWidget)
  : Superclass( parentWidget )
  , d_ptr( new qSlicerPointSetProcessingCppFooBarWidgetPrivate(*this) )
{
  Q_D(qSlicerPointSetProcessingCppFooBarWidget);
  d->setupUi(this);
}

//-----------------------------------------------------------------------------
qSlicerPointSetProcessingCppFooBarWidget
::~qSlicerPointSetProcessingCppFooBarWidget()
{
}
