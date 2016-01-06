import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

import logging

class PointSetProcessingPy(ScriptedLoadableModule):
  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "PointSetProcessing" 
    self.parent.categories = ["IGT"]
    self.parent.dependencies = []
    self.parent.contributors = ["Mikael Brudfors (2015 The Biomedical Imaging and Instrumentation Group (BiiG) of the University Carlos III de Madrid (https://image.hggm.es/)"]
    self.parent.helpText = """
    This module reconstructs a surface from unorganized points. For more information see: https://github.com/brudfors/SlicerPointSetProcessing
    """
    self.parent.acknowledgementText = """
    Supported by projects IPT-2012-0401-300000, TEC2013-48251-C2-1-R, DTS14/00192 and FEDER funds. 
"""

class PointSetProcessingPyWidget(ScriptedLoadableModuleWidget):
  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    pointSetProcessingCollapsibleButton = ctk.ctkCollapsibleButton()
    pointSetProcessingCollapsibleButton.text = "Surface Reconstruction from Unorganized Points"
    self.layout.addWidget(pointSetProcessingCollapsibleButton)
    pointSetProcessingFormLayout = qt.QFormLayout(pointSetProcessingCollapsibleButton)

    # Input
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ( ("vtkMRMLModelNode"), "" )
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    pointSetProcessingFormLayout.addRow("Input Model: ", self.inputSelector)
    
    self.nbrOfPointsLabel = qt.QLabel('Number of Points in Input Model: - ')
    pointSetProcessingFormLayout.addRow(self.nbrOfPointsLabel)

    self.inputPointSizeSlider = ctk.ctkSliderWidget()
    self.inputPointSizeSlider.setDecimals(0)
    self.inputPointSizeSlider.singleStep = 1
    self.inputPointSizeSlider.minimum = 1
    self.inputPointSizeSlider.maximum = 10
    self.inputPointSizeSlider.value = 1
    pointSetProcessingFormLayout.addRow('Input Model Point Size: ', self.inputPointSizeSlider)
    
    # Runtime
    self.runtimeGroupBox = qt.QGroupBox('Runtime')    
    runtimeFormLayout = qt.QFormLayout(self.runtimeGroupBox)
    pointSetProcessingFormLayout.addRow(self.runtimeGroupBox)
    
    self.runtimeLabel = qt.QLabel()
    self.runtimeLabel.setText("... s.")
    self.runtimeLabel.setWordWrap(True)
    self.runtimeLabel.setStyleSheet("QLabel { background-color : black; \
                                           color : #66FF00; \
                                           height : 60px; \
                                           border-style: outset; \
                                           border-width: 5px; \
                                           border-radius: 10px; \
                                           font: bold 14px; \
                                           padding: 0px;\
                                           font-family : SimSun; \
                                           qproperty-alignment: AlignCenter}")
    runtimeFormLayout.addRow(self.runtimeLabel)    
    
    # Downsample
    self.downSampleGroupBox = ctk.ctkCollapsibleGroupBox()
    self.downSampleGroupBox.setTitle("Downsample Input Model")
    downSampleFormLayout = qt.QFormLayout(self.downSampleGroupBox)
    pointSetProcessingFormLayout.addRow(self.downSampleGroupBox)    
    
    self.toleranceCleanSlider = ctk.ctkSliderWidget()
    self.toleranceCleanSlider.setDecimals(2)
    self.toleranceCleanSlider.singleStep = 0.01
    self.toleranceCleanSlider.minimum = 0.0
    self.toleranceCleanSlider.maximum = 1.0
    self.toleranceCleanSlider.value = 0.01
    self.toleranceCleanSlider.setToolTip('')
    self.toleranceCleanSlider.enabled = True
    downSampleFormLayout.addRow('Tolerance: ', self.toleranceCleanSlider)
    
    self.vtkCleanPolyDataButton = qt.QPushButton("Apply")
    self.vtkCleanPolyDataButton.enabled = False
    self.vtkCleanPolyDataButton.checkable = True
    downSampleFormLayout.addRow(self.vtkCleanPolyDataButton)    

    # Outlier Removal
    self.outlierRemovalGroupBox = ctk.ctkCollapsibleGroupBox()
    self.outlierRemovalGroupBox.setTitle("Outlier Removal")
    outlierRemovalFormLayout = qt.QFormLayout(self.outlierRemovalGroupBox)
    pointSetProcessingFormLayout.addRow(self.outlierRemovalGroupBox)
    
    self.percentToRemoveSlider = ctk.ctkSliderWidget()
    self.percentToRemoveSlider.setDecimals(2)
    self.percentToRemoveSlider.singleStep = 0.01
    self.percentToRemoveSlider.minimum = 0.0
    self.percentToRemoveSlider.maximum = 1.0
    self.percentToRemoveSlider.value = 0.01
    self.percentToRemoveSlider.setToolTip('')
    self.percentToRemoveSlider.enabled = True
    outlierRemovalFormLayout.addRow('Percent to Remove: ', self.percentToRemoveSlider)
    
    self.vtkPointSetOutlierRemovalButton = qt.QPushButton("Apply")
    self.vtkPointSetOutlierRemovalButton.enabled = False
    self.vtkPointSetOutlierRemovalButton.checkable = True
    outlierRemovalFormLayout.addRow(self.vtkPointSetOutlierRemovalButton)  
        
    # Compute Normals
    self.normalsGroupBox = ctk.ctkCollapsibleGroupBox()
    self.normalsGroupBox.setTitle("Compute Normals")
    normalsFormLayout = qt.QFormLayout(self.normalsGroupBox)
    pointSetProcessingFormLayout.addRow(self.normalsGroupBox)
    
    self.normalsTabWidget = qt.QTabWidget()
    normalsFormLayout.addRow(self.normalsTabWidget)

    # vtkPointSetNormalEstimationAndOrientation
    self.vtkPointSetNormalEstimationWidget = qt.QWidget()
    vtkPointSetNormalEstimationFormLayout = qt.QFormLayout(self.vtkPointSetNormalEstimationWidget)
    normalsFormLayout.addRow(self.vtkPointSetNormalEstimationWidget)
    self.normalsTabWidget.addTab(self.vtkPointSetNormalEstimationWidget, "vtkPointSetNormalEstimationAndOrientation")    
        
    self.modeTypeComboBox = qt.QComboBox()
    self.modeTypeComboBox.addItem('Fixed')  
    self.modeTypeComboBox.addItem('Radius')
    self.modeTypeComboBox.setCurrentIndex(1)
    self.modeTypeComboBox.setToolTip('')    
    vtkPointSetNormalEstimationFormLayout.addRow('Mode Type: ', self.modeTypeComboBox)
    
    self.numberOfNeighborsSlider = ctk.ctkSliderWidget()
    self.numberOfNeighborsSlider.setDecimals(0)
    self.numberOfNeighborsSlider.singleStep = 1
    self.numberOfNeighborsSlider.minimum = 1
    self.numberOfNeighborsSlider.maximum = 20
    self.numberOfNeighborsSlider.value = 4
    self.numberOfNeighborsSlider.setToolTip('')
    self.numberOfNeighborsSlider.enabled = False
    vtkPointSetNormalEstimationFormLayout.addRow('Fixed Neighbors: ', self.numberOfNeighborsSlider)
    
    self.radiusSlider = ctk.ctkSliderWidget()
    self.radiusSlider.setDecimals(2)
    self.radiusSlider.singleStep = 0.01
    self.radiusSlider.minimum = 0
    self.radiusSlider.maximum = 50
    self.radiusSlider.value = 1.0
    self.radiusSlider.setToolTip('')
    vtkPointSetNormalEstimationFormLayout.addRow('Radius: ', self.radiusSlider)
    
    self.graphTypeComboBox = qt.QComboBox()
    self.graphTypeComboBox.addItem('Riemann')  
    self.graphTypeComboBox.addItem('KNN')
    self.graphTypeComboBox.setCurrentIndex(1)
    self.graphTypeComboBox.setToolTip('')    
    vtkPointSetNormalEstimationFormLayout.addRow('Graph Type: ', self.graphTypeComboBox)
    
    self.knnSlider = ctk.ctkSliderWidget()
    self.knnSlider.setDecimals(0)
    self.knnSlider.singleStep = 1
    self.knnSlider.minimum = 1
    self.knnSlider.maximum = 100
    self.knnSlider.value = 5
    self.knnSlider.setToolTip('')
    vtkPointSetNormalEstimationFormLayout.addRow('K-Nearest Neighbors: ', self.knnSlider)
    
    self.vtkPointSetNormalEstimationButton = qt.QPushButton("Apply")
    self.vtkPointSetNormalEstimationButton.enabled = False
    self.vtkPointSetNormalEstimationButton.checkable = True
    vtkPointSetNormalEstimationFormLayout.addRow(self.vtkPointSetNormalEstimationButton)    

    # vtkPolyDataNormals
    self.vtkPolyDataNormalsWidget = qt.QWidget()
    vtkPolyDataNormalsFormLayout = qt.QFormLayout(self.vtkPolyDataNormalsWidget)
    normalsFormLayout.addRow(self.vtkPolyDataNormalsWidget)
    self.normalsTabWidget.addTab(self.vtkPolyDataNormalsWidget, "vtkPolyDataNormals")    
    
    self.featureAngleSlider = ctk.ctkSliderWidget()
    self.featureAngleSlider.setDecimals(2)
    self.featureAngleSlider.singleStep = 0.01
    self.featureAngleSlider.minimum = 0
    self.featureAngleSlider.maximum = 360
    self.featureAngleSlider.value = 0.1
    self.featureAngleSlider.setToolTip('')
    vtkPolyDataNormalsFormLayout.addRow('Feature Angle: ', self.featureAngleSlider)    
    
    self.splittingComboBox = qt.QComboBox()
    self.splittingComboBox.addItem('False')
    self.splittingComboBox.addItem('True')  
    self.splittingComboBox.setCurrentIndex(1)
    self.splittingComboBox.setToolTip('')    
    vtkPolyDataNormalsFormLayout.addRow('Splitting: ', self.splittingComboBox)
    
    self.consistencyComboBox = qt.QComboBox()
    self.consistencyComboBox.addItem('False')
    self.consistencyComboBox.addItem('True')  
    self.consistencyComboBox.setCurrentIndex(0)
    self.consistencyComboBox.setToolTip('')    
    vtkPolyDataNormalsFormLayout.addRow('Consistency: ', self.consistencyComboBox)
    
    self.autoOrientNormalsComboBox = qt.QComboBox()
    self.autoOrientNormalsComboBox.addItem('False')
    self.autoOrientNormalsComboBox.addItem('True') 
    self.autoOrientNormalsComboBox.setCurrentIndex(0)    
    self.autoOrientNormalsComboBox.setToolTip('')    
    vtkPolyDataNormalsFormLayout.addRow('Auto-Orient Normals: ', self.autoOrientNormalsComboBox)
    
    self.computePointNormalsComboBox = qt.QComboBox()
    self.computePointNormalsComboBox.addItem('False')
    self.computePointNormalsComboBox.addItem('True') 
    self.computePointNormalsComboBox.setCurrentIndex(1)    
    self.computePointNormalsComboBox.setToolTip('')    
    vtkPolyDataNormalsFormLayout.addRow('Compute Point Normals: ', self.computePointNormalsComboBox)
    
    self.computeCellNormalsComboBox = qt.QComboBox()
    self.computeCellNormalsComboBox.addItem('False')
    self.computeCellNormalsComboBox.addItem('True')
    self.computeCellNormalsComboBox.setCurrentIndex(0)    
    self.computeCellNormalsComboBox.setToolTip('')    
    vtkPolyDataNormalsFormLayout.addRow('Compute Cell Normals: ', self.computeCellNormalsComboBox)
    
    self.flipNormalsComboBox = qt.QComboBox()
    self.flipNormalsComboBox.addItem('False')
    self.flipNormalsComboBox.addItem('True')  
    self.flipNormalsComboBox.setCurrentIndex(0)
    self.flipNormalsComboBox.setToolTip('')    
    vtkPolyDataNormalsFormLayout.addRow('Flip Normals: ', self.flipNormalsComboBox)
    
    self.nonManifoldTraversalComboBox = qt.QComboBox()
    self.nonManifoldTraversalComboBox.addItem('False')
    self.nonManifoldTraversalComboBox.addItem('True') 
    self.nonManifoldTraversalComboBox.setCurrentIndex(1)    
    self.nonManifoldTraversalComboBox.setToolTip('')    
    vtkPolyDataNormalsFormLayout.addRow('Non-Manifold Traversal: ', self.nonManifoldTraversalComboBox)
    
    self.vtkPolyDataNormalsButton = qt.QPushButton("Apply")
    self.vtkPolyDataNormalsButton.enabled = False
    self.vtkPolyDataNormalsButton.checkable = True
    vtkPolyDataNormalsFormLayout.addRow(self.vtkPolyDataNormalsButton)  
    
    self.normalsVisibleCheckBox = qt.QCheckBox('Arrows Visibility: ')
    self.normalsVisibleCheckBox.checked = True
    self.normalsVisibleCheckBox.enabled = True
    self.normalsVisibleCheckBox.setLayoutDirection(1)
    normalsFormLayout.addRow(self.normalsVisibleCheckBox)
    
    # Compute Surface
    self.surfaceGroupBox = ctk.ctkCollapsibleGroupBox()
    self.surfaceGroupBox.setTitle("Compute Surface")
    surfaceFormLayout = qt.QFormLayout(self.surfaceGroupBox)
    pointSetProcessingFormLayout.addRow(self.surfaceGroupBox)

    self.surfaceTabWidget = qt.QTabWidget()
    surfaceFormLayout.addRow(self.surfaceTabWidget)
    
    # vtkPoissionReconstruction    
    self.vtkPoissionReconstructionWidget = qt.QWidget()
    vtkPoissionReconstructionFormLayout = qt.QFormLayout(self.vtkPoissionReconstructionWidget)
    surfaceFormLayout.addRow(self.vtkPoissionReconstructionWidget)
    self.surfaceTabWidget.addTab(self.vtkPoissionReconstructionWidget, "vtkPoissionReconstruction")   
    
    self.depthSlider = ctk.ctkSliderWidget()
    self.depthSlider.setDecimals(0)
    self.depthSlider.singleStep = 1
    self.depthSlider.minimum = 1
    self.depthSlider.maximum = 14
    self.depthSlider.value = 8
    self.depthSlider.setToolTip('This integer controls the reconstruction depth; the maximum depth of the tree that will be used for surface reconstruction. Running at depth d corresponds to solving on a voxel grid whose resolution is no larger than 2^d x 2^d x 2^d. Note that since the reconstructor adapts the octree to the sampling density, the specified reconstruction depth is only an upper bound.')
    vtkPoissionReconstructionFormLayout.addRow('Depth: ', self.depthSlider)
    
    self.scaleSlider = ctk.ctkSliderWidget()
    self.scaleSlider.setDecimals(2)
    self.scaleSlider.singleStep = 0.01
    self.scaleSlider.minimum = 0
    self.scaleSlider.maximum = 10
    self.scaleSlider.value = 1.25
    self.scaleSlider.setToolTip('This floating point value specifies the ratio between the diameter of the cube used for reconstruction and the diameter of the samples bounding cube.')
    vtkPoissionReconstructionFormLayout.addRow('Scale: ', self.scaleSlider)    
    
    self.solverDivideSlider = ctk.ctkSliderWidget()
    self.solverDivideSlider.setDecimals(0)
    self.solverDivideSlider.singleStep = 1
    self.solverDivideSlider.minimum = 1
    self.solverDivideSlider.maximum = 20
    self.solverDivideSlider.value = 8
    self.solverDivideSlider.setToolTip('Solver subdivision depth; This integer argument specifies the depth at which a block Gauss-Seidel solver is used to solve the Laplacian equation. Using this parameter helps reduce the memory overhead at the cost of a small increase in reconstruction time. (In practice, we have found that for reconstructions of depth 9 or higher a subdivide depth of 7 or 8 can greatly reduce the memory usage.)')
    vtkPoissionReconstructionFormLayout.addRow('Solver Divide: ', self.solverDivideSlider)   
    
    self.isoDivideSlider = ctk.ctkSliderWidget()
    self.isoDivideSlider.setDecimals(0)
    self.isoDivideSlider.singleStep = 1
    self.isoDivideSlider.minimum = 1
    self.isoDivideSlider.maximum = 20
    self.isoDivideSlider.value = 8
    self.isoDivideSlider.setToolTip('Iso-surface extraction subdivision depth; This integer argument specifies the depth at which a block isosurface extractor should be used to extract the iso-surface. Using this parameter helps reduce the memory overhead at the cost of a small increase in extraction time. (In practice, we have found that for reconstructions of depth 9 or higher a subdivide depth of 7 or 8 can greatly reduce the memory usage.)')
    vtkPoissionReconstructionFormLayout.addRow('Iso Divide: ', self.isoDivideSlider)   
 
    self.samplesPerNodeSlider = ctk.ctkSliderWidget()
    self.samplesPerNodeSlider.setDecimals(2)
    self.samplesPerNodeSlider.singleStep = 0.1
    self.samplesPerNodeSlider.minimum = 1
    self.samplesPerNodeSlider.maximum = 30
    self.samplesPerNodeSlider.value = 1.0
    self.samplesPerNodeSlider.setToolTip('Minimum number of samples; This floating point value specifies the minimum number of sample points that should fall within an octree node as the octree construction is adapted to sampling density. For noise-free samples, small values in the range [1.0 - 5.0] can be used. For more noisy samples, larger values in the range [15.0 - 20.0] may be needed to provide a smoother, noise-reduced, reconstruction.')
    vtkPoissionReconstructionFormLayout.addRow('Samples per Node: ', self.samplesPerNodeSlider)   
    
    self.confidenceComboBox = qt.QComboBox()
    self.confidenceComboBox.addItem('False')
    self.confidenceComboBox.addItem('True')  
    self.confidenceComboBox.setToolTip('Enabling tells the reconstructor to use the size of the normals as confidence information. When the flag is not enabled, all normals are normalized to have unit-length prior to reconstruction.')    
    vtkPoissionReconstructionFormLayout.addRow('Confidence: ', self.confidenceComboBox)
   
    self.verboseComboBox = qt.QComboBox()
    self.verboseComboBox.addItem('False')
    self.verboseComboBox.addItem('True')  
    self.verboseComboBox.setToolTip('Enabling this flag provides a more verbose description of the running times and memory usages of individual components of the surface reconstructor.')    
    vtkPoissionReconstructionFormLayout.addRow('Verbose: ', self.verboseComboBox)
    
    self.vtkPoissionReconstructionButton = qt.QPushButton("Apply")
    self.vtkPoissionReconstructionButton.enabled = False
    self.vtkPoissionReconstructionButton.checkable = True
    vtkPoissionReconstructionFormLayout.addRow(self.vtkPoissionReconstructionButton)    

    # vtkDelaunay3D
    self.vtkDelaunay3DWidget = qt.QWidget()
    vtkDelaunay3DFormLayout = qt.QFormLayout(self.vtkDelaunay3DWidget)
    surfaceFormLayout.addRow(self.vtkDelaunay3DWidget)
    self.surfaceTabWidget.addTab(self.vtkDelaunay3DWidget, "vtkDelaunay3D") 
    
    self.alphaSlider = ctk.ctkSliderWidget()
    self.alphaSlider.setDecimals(1)
    self.alphaSlider.singleStep = 0.1
    self.alphaSlider.minimum = 0.0
    self.alphaSlider.maximum = 100.0
    self.alphaSlider.value = 0.0
    self.alphaSlider.setToolTip('')
    vtkDelaunay3DFormLayout.addRow('Alpha: ', self.alphaSlider)   
    
    self.toleranceSlider = ctk.ctkSliderWidget()
    self.toleranceSlider.setDecimals(2)
    self.toleranceSlider.singleStep = 0.01
    self.toleranceSlider.minimum = 0.0
    self.toleranceSlider.maximum = 1.0
    self.toleranceSlider.value = 0.0
    self.toleranceSlider.setToolTip('')
    vtkDelaunay3DFormLayout.addRow('Tolerance: ', self.toleranceSlider)   
    
    self.offsetSlider = ctk.ctkSliderWidget()
    self.offsetSlider.setDecimals(1)
    self.offsetSlider.singleStep = 0.1
    self.offsetSlider.minimum = 0.0
    self.offsetSlider.maximum = 10.0
    self.offsetSlider.value = 2.5
    self.offsetSlider.setToolTip('')
    vtkDelaunay3DFormLayout.addRow('Offset: ', self.offsetSlider)   
    
    self.boundingComboBox = qt.QComboBox()
    self.boundingComboBox.addItem('False')
    self.boundingComboBox.addItem('True')  
    self.boundingComboBox.setCurrentIndex(0)    
    self.boundingComboBox.setToolTip('')    
    vtkDelaunay3DFormLayout.addRow('Bounding Triangulations: ', self.boundingComboBox)
    
    self.vtkDelaunay3DButton = qt.QPushButton("Apply")
    self.vtkDelaunay3DButton.enabled = False
    self.vtkDelaunay3DButton.checkable = True
    vtkDelaunay3DFormLayout.addRow(self.vtkDelaunay3DButton)    
    
    self.surfaceVisibleCheckBox = qt.QCheckBox('Surface Visibility: ')
    self.surfaceVisibleCheckBox.checked = True
    self.surfaceVisibleCheckBox.enabled = True
    self.surfaceVisibleCheckBox.setLayoutDirection(1)
    surfaceFormLayout.addRow(self.surfaceVisibleCheckBox)
    
    # connections
    self.vtkCleanPolyDataButton.connect('clicked(bool)', self.vtkCleanPolyDataClicked)
    self.vtkPointSetOutlierRemovalButton.connect('clicked(bool)', self.vtkPointSetOutlierRemovalClicked)
    self.vtkPointSetNormalEstimationButton.connect('clicked(bool)', self.vtkPointSetNormalEstimationClicked)
    self.vtkPolyDataNormalsButton.connect('clicked(bool)', self.vtkPolyDataNormalsClicked)
    self.vtkPoissionReconstructionButton.connect('clicked(bool)', self.vtkPoissionReconstructionClicked)
    self.vtkDelaunay3DButton.connect('clicked(bool)', self.vtkDelaunay3DClicked)
    self.inputSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSelect)
    self.graphTypeComboBox.connect('currentIndexChanged(const QString &)', self.onGraphTypeChanged)
    self.modeTypeComboBox.connect('currentIndexChanged(const QString &)', self.onModeChanged)
    self.surfaceVisibleCheckBox.connect('stateChanged(int)', self.onSurfaceVisible)
    self.normalsVisibleCheckBox.connect('stateChanged(int)', self.onNormalsVisible)
    self.inputPointSizeSlider.connect('valueChanged (double)', self.onInputPointSliderModified)
            
    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh 
    self.onSelect()
        
    lm=slicer.app.layoutManager()
    lm.setLayout(4) # One 3D-view    

  def onInputPointSliderModified(self, value):
    inputModelNode = self.inputSelector.currentNode()
    if inputModelNode:
      inputModelNode.GetModelDisplayNode().SetPointSize(value)
  
  def onSurfaceVisible(self, state):
    logic = PointSetProcessingPyLogic()
    logic.setModelVisibility('ComputedSurface', self.surfaceVisibleCheckBox.checked)
 
  def onNormalsVisible(self, state):
    logic = PointSetProcessingPyLogic()
    logic.setModelVisibility('OrientatedGlyphs', self.normalsVisibleCheckBox.checked)
    
  def onGraphTypeChanged(self, type):
    if type == 'KNN':
      self.knnSlider.enabled = True
    elif type == 'Riemann':
      self.knnSlider.enabled = False

  def onModeChanged(self, type):
    if type == 'Radius':
      self.radiusSlider.enabled = True
      self.numberOfNeighborsSlider.enabled = False
    elif type == 'Fixed':
      self.radiusSlider.enabled = False
      self.numberOfNeighborsSlider.enabled = True
      
  def onSelect(self):
    self.vtkCleanPolyDataButton.enabled = self.inputSelector.currentNode()
    self.vtkPointSetNormalEstimationButton.enabled = self.inputSelector.currentNode()
    self.vtkPoissionReconstructionButton.enabled = self.inputSelector.currentNode()
    self.vtkPolyDataNormalsButton.enabled = self.inputSelector.currentNode()
    self.vtkDelaunay3DButton.enabled = self.inputSelector.currentNode()
    self.vtkPointSetOutlierRemovalButton.enabled = self.inputSelector.currentNode()
    if self.inputSelector.currentNode():
      self.inputSelector.currentNode().GetModelDisplayNode().SetPointSize(self.inputPointSizeSlider.value)

  def vtkPointSetOutlierRemovalClicked(self):
    if self.vtkPointSetOutlierRemovalButton.checked:
      logic = PointSetProcessingPyLogic()  
      logic.vtkPointSetOutlierRemoval(self.inputSelector.currentNode(), self.percentToRemoveSlider.value, self.runtimeLabel)
      self.vtkPointSetOutlierRemovalButton.checked = False
      self.nbrOfPointsLabel.setText('Number of Points in Input Model: ' + str(self.inputSelector.currentNode().GetPolyData().GetNumberOfPoints()))    
    
  def vtkDelaunay3DClicked(self):
    if self.vtkDelaunay3DButton.checked:
      logic = PointSetProcessingPyLogic()  
      logic.vtkDelaunay3D(self.inputSelector.currentNode(), self.alphaSlider.value, self.toleranceSlider.value, self.offsetSlider.value, self.boundingComboBox.currentIndex, self.runtimeLabel)
      self.vtkDelaunay3DButton.checked = False    
  
  def vtkCleanPolyDataClicked(self):
    if self.vtkCleanPolyDataButton.checked:
      logic = PointSetProcessingPyLogic()
      logic.vtkCleanPolyData(self.inputSelector.currentNode(), self.toleranceCleanSlider.value, self.runtimeLabel)        
      self.vtkCleanPolyDataButton.checked = False   
      self.nbrOfPointsLabel.setText('Number of Points in Input Model: ' + str(self.inputSelector.currentNode().GetPolyData().GetNumberOfPoints()))
      
  def vtkPointSetNormalEstimationClicked(self):
    if self.vtkPointSetNormalEstimationButton.checked:
      logic = PointSetProcessingPyLogic()
      logic.vtkPointSetNormalEstimation(self.inputSelector.currentNode(), self.modeTypeComboBox.currentIndex, self.numberOfNeighborsSlider.value, self.radiusSlider.value, self.knnSlider.value, self.graphTypeComboBox.currentIndex, self.runtimeLabel)        
      self.vtkPointSetNormalEstimationButton.checked = False   
  
  def vtkPolyDataNormalsClicked(self):
    if self.vtkPolyDataNormalsButton.checked:
      logic = PointSetProcessingPyLogic()
      logic.vtkPolyDataNormals(self.inputSelector.currentNode(), self.featureAngleSlider.value, self.splittingComboBox.currentIndex, self.consistencyComboBox.currentIndex, self.autoOrientNormalsComboBox.currentIndex, self.computePointNormalsComboBox.currentIndex, self.computeCellNormalsComboBox.currentIndex, self.flipNormalsComboBox.currentIndex, self.nonManifoldTraversalComboBox.currentIndex, self.runtimeLabel)        
      self.vtkPolyDataNormalsButton.checked = False   
  
  def vtkPoissionReconstructionClicked(self):
    if self.vtkPoissionReconstructionButton.checked:
      logic = PointSetProcessingPyLogic()  
      logic.vtkPoissionReconstruction(self.depthSlider.value, self.scaleSlider.value, self.solverDivideSlider.value, self.isoDivideSlider.value, self.samplesPerNodeSlider.value, self.confidenceComboBox.currentIndex, self.verboseComboBox.currentIndex, self.runtimeLabel)
      self.vtkPoissionReconstructionButton.checked = False         

class PointSetProcessingPyLogic(ScriptedLoadableModuleLogic):

  def vtkCleanPolyData(self, inputModelNode, tolerance, runtimeLabel):
    runtime = vtk.vtkTimerLog()
    runtime.StartTimer()
    # vtkVertexGlyphFilter
    glyphFilter = vtk.vtkVertexGlyphFilter()
    glyphFilter.SetInputConnection(inputModelNode.GetPolyDataConnection())
    # vtkCleanPolyData
    cleanPolyData = vtk.vtkCleanPolyData()
    cleanPolyData.SetInputConnection(glyphFilter.GetOutputPort())
    cleanPolyData.SetTolerance(tolerance)
    cleanPolyData.Update()
    runtime.StopTimer()
    runtimeLabel.setText('vtkCleanPolyData computed in  %.2f' % runtime.GetElapsedTime() + ' s.')    
    inputModelNode.SetAndObservePolyData(cleanPolyData.GetOutput())
  
  def vtkPointSetOutlierRemoval(self, inputModelNode, percentToRemove, runtimeLabel):
    runtime = slicer.modules.pointsetprocessingcpp.logic().Apply_vtkPointSetOutlierRemoval(inputModelNode, float(percentToRemove), True)
    runtimeLabel.setText('vtkPointSetOutlierRemoval computed in  %.2f' % runtime + ' s.')
    
  def vtkPointSetNormalEstimation(self, inputModelNode, mode, numberOfNeighbors, radius, kNearestNeighbors, graphType, runtimeLabel):
    outputModelNode = slicer.util.getNode('ComputedNormals')
    if not outputModelNode:
      outputModelNode = self.createModelNode('ComputedNormals', [0, 0, 1])  
      outputModelNode.SetDisplayVisibility(False)
    orientatedGlyphs = slicer.util.getNode('OrientatedGlyphs')
    if not orientatedGlyphs:
      orientatedGlyphs = self.createModelNode('OrientatedGlyphs', [0, 1, 0])        
    runtime = slicer.modules.pointsetprocessingcpp.logic().Apply_vtkPointSetNormalEstimation(inputModelNode, outputModelNode, orientatedGlyphs, int(mode), int(numberOfNeighbors), float(radius), int(kNearestNeighbors), int(graphType), True, True)
    runtimeLabel.setText('vtkPointSetNormalEstimation computed in  %.2f' % runtime + ' s.')
    return True
   
  def vtkPolyDataNormals(self, inputModelNode, featureAngle, splitting, consistency, autoOrientNormals, computePointNormals, computeCellNormals, flipNormals, nonManifoldTraversal, runtimeLabel):
    outputModelNode = slicer.util.getNode('ComputedNormals')
    if not outputModelNode:
      outputModelNode = self.createModelNode('ComputedNormals', [0, 0, 1])  
      outputModelNode.SetDisplayVisibility(False)
    orientatedGlyphs = slicer.util.getNode('OrientatedGlyphs')
    if not orientatedGlyphs:
      orientatedGlyphs = self.createModelNode('OrientatedGlyphs', [0, 1, 0])    
    runtime = slicer.modules.pointsetprocessingcpp.logic().Apply_vtkPolyDataNormals(inputModelNode, outputModelNode, orientatedGlyphs, float(featureAngle), splitting, consistency, autoOrientNormals, computePointNormals, computeCellNormals, flipNormals, nonManifoldTraversal, True, True)
    runtimeLabel.setText('vtkPolyDataNormals computed in  %.2f' % runtime + ' s.')
    return True
   
  def vtkDelaunay3D(self, inputModelNode, alpha, tolerance, offset, boudingTriangulation, runtimeLabel):
    outputModelNode = slicer.util.getNode('ComputedSurface')
    if not outputModelNode:
      outputModelNode = self.createModelNode('ComputedSurface', [1, 0, 0])
    runtime = slicer.modules.pointsetprocessingcpp.logic().Apply_vtkDelaunay3D(inputModelNode, outputModelNode, float(alpha), float(tolerance), float(offset), boudingTriangulation, True)
    runtimeLabel.setText('vtkDelaunay3D computed in %.2f' % runtime + ' s.')
    return True

  def vtkPoissionReconstruction(self, depth, scale, solverDivide, isoDivide, samplesPerNode, confidence, verbose, runtimeLabel):
    inputModelNode = slicer.util.getNode('ComputedNormals')
    outputModelNode = slicer.util.getNode('ComputedSurface')
    if not outputModelNode:
      outputModelNode = self.createModelNode('ComputedSurface', [1, 0, 0])
    runtime = slicer.modules.pointsetprocessingcpp.logic().Apply_vtkPoissionReconstruction(inputModelNode, outputModelNode, int(depth), float(scale), int(solverDivide), int(isoDivide), float(samplesPerNode), int(confidence), int(verbose), True)
    runtimeLabel.setText('vtkPoissionReconstruction computed in %.2f' % runtime + ' s.')
    return True
    
  def setModelVisibility(self, name, visible):
    modelNode = slicer.util.getNode(name)
    if modelNode:  
      modelNode.SetDisplayVisibility(visible)
    
  def createModelNode(self, name, color):
    scene = slicer.mrmlScene
    modelNode = slicer.vtkMRMLModelNode()
    modelNode.SetScene(scene)
    modelNode.SetName(name)
    modelDisplay = slicer.vtkMRMLModelDisplayNode()
    modelDisplay.SetColor(color)
    modelDisplay.SetScene(scene)
    scene.AddNode(modelDisplay)
    modelNode.SetAndObserveDisplayNodeID(modelDisplay.GetID())
    scene.AddNode(modelNode)  
    return modelNode
