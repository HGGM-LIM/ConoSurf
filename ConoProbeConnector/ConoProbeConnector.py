import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

import csv
import logging
import os
import time
    
class ConoProbeConnector(ScriptedLoadableModule):

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "ConoProbeConnector" # TODO make this more human readable by adding spaces
    self.parent.categories = ["LIM Modules"]
    self.parent.dependencies = []
    self.parent.contributors = ["Mikael Brudfors (CMIC, UCL, London, UK)"] 
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    It performs a simple thresholding on the input volume and optionally captures a screenshot.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

######################################################## ConoProbeConnectorWidget
class ConoProbeConnectorWidget(ScriptedLoadableModuleWidget):

  ######################################################## Setup
  def setup(self):
    self.conoProbeConnectorLogic = ConoProbeConnectorLogic() 
    self.firstInitColouring = True
    
    ScriptedLoadableModuleWidget.setup(self)
  
    # Icons stuff
    self.conoProbeConnectorModuleDirectoryPath = slicer.modules.conoprobeconnector.path.replace("ConoProbeConnector.py","")
    self.playIcon = qt.QIcon(self.conoProbeConnectorModuleDirectoryPath + '/Resources/Icons/playIcon.png')
    self.stopIcon = qt.QIcon(self.conoProbeConnectorModuleDirectoryPath + '/Resources/Icons/stopIcon.png')
    self.recordIcon = qt.QIcon(self.conoProbeConnectorModuleDirectoryPath + '/Resources/Icons/recordIcon.png')
    self.restartIcon = qt.QIcon(self.conoProbeConnectorModuleDirectoryPath + '/Resources/Icons/restartIcon.png')
    self.saveIcon = qt.QIcon(self.conoProbeConnectorModuleDirectoryPath + '/Resources/Icons/saveIcon.png')                         
    
    self.errorStyleSheet = "QLabel { color : #FF0000; \
                                     font: bold 14px}"
    self.defaultStyleSheet = "QLabel { color : #000000; \
                                       font: bold 14px}"     
                                  
    ######################################################## Recorder
    recorderCollapsibleButton = ctk.ctkCollapsibleButton()
    recorderCollapsibleButton.text = "ConoProbe Connector"
    recorderCollapsibleButton.collapsed = False
    self.layout.addWidget(recorderCollapsibleButton)
    recorderFormLayout = qt.QFormLayout(recorderCollapsibleButton)
    
    # Output
    self.recorderOutputGroupBox = ctk.ctkCollapsibleGroupBox()
    self.recorderOutputGroupBox.setTitle("Output")
    recorderOutputFormLayout = qt.QFormLayout(self.recorderOutputGroupBox)
    recorderFormLayout.addRow(self.recorderOutputGroupBox)
    
    self.lensMinLabel = qt.QLabel('-')
    self.lensMinLabel.setStyleSheet(self.defaultStyleSheet)
    self.QFormLayoutLeftLabel10 = qt.QLabel('Lens Min. Dist. (mm): ')
    self.QFormLayoutLeftLabel10.setStyleSheet(self.defaultStyleSheet)
    recorderOutputFormLayout.addRow(self.QFormLayoutLeftLabel10, self.lensMinLabel) 
    
    self.distanceLabel = qt.QLabel('-')
    self.distanceLabel.setStyleSheet(self.defaultStyleSheet)
    self.QFormLayoutLeftLabel1 = qt.QLabel('Distance (mm): ')
    self.QFormLayoutLeftLabel1.setStyleSheet(self.defaultStyleSheet)
    recorderOutputFormLayout.addRow(self.QFormLayoutLeftLabel1, self.distanceLabel)  

    self.lensMaxLabel = qt.QLabel('-')
    self.lensMaxLabel.setStyleSheet(self.defaultStyleSheet)
    self.QFormLayoutLeftLabel11 = qt.QLabel('Lens Max. Dist. (mm): ')
    self.QFormLayoutLeftLabel11.setStyleSheet(self.defaultStyleSheet)
    recorderOutputFormLayout.addRow(self.QFormLayoutLeftLabel11, self.lensMaxLabel) 
    
    dummyLabel1 = qt.QLabel('')
    recorderOutputFormLayout.addRow('', dummyLabel1)
    
    self.powerLabel = qt.QLabel('-')
    self.powerLabel.setStyleSheet(self.defaultStyleSheet)
    self.QFormLayoutLeftLabel8 = qt.QLabel('Laser Power (arb. unit): ')
    self.QFormLayoutLeftLabel8.setStyleSheet(self.defaultStyleSheet)
    recorderOutputFormLayout.addRow(self.QFormLayoutLeftLabel8, self.powerLabel)  

    self.frequencyLabel = qt.QLabel('-')
    self.frequencyLabel.setStyleSheet(self.defaultStyleSheet)
    self.QFormLayoutLeftLabel9 = qt.QLabel('Laser Frequency (Hz): ')
    self.QFormLayoutLeftLabel9.setStyleSheet(self.defaultStyleSheet)
    recorderOutputFormLayout.addRow(self.QFormLayoutLeftLabel9, self.frequencyLabel)  
   
    self.nbrOfPointsRecordedLabel = qt.QLabel('0')
    self.nbrOfPointsRecordedLabel.setStyleSheet(self.defaultStyleSheet)
    self.QFormLayoutLeftLabel2 = qt.QLabel('Nbr. of Points Recorded: ')
    self.QFormLayoutLeftLabel2.setStyleSheet(self.defaultStyleSheet)
    recorderOutputFormLayout.addRow(self.QFormLayoutLeftLabel2, self.nbrOfPointsRecordedLabel)
    
    self.positionLabel = qt.QLabel('-')
    self.positionLabel.setStyleSheet(self.defaultStyleSheet)
    self.QFormLayoutLeftLabel3 = qt.QLabel('Position ([r, a, s]): ')
    self.QFormLayoutLeftLabel3.setStyleSheet(self.defaultStyleSheet)
    recorderOutputFormLayout.addRow(self.QFormLayoutLeftLabel3, self.positionLabel)   
    
    self.timeLabel = qt.QLabel('-')
    self.timeLabel.setStyleSheet(self.defaultStyleSheet)
    self.QFormLayoutLeftLabel4 = qt.QLabel('Recording Time (s): ')
    self.QFormLayoutLeftLabel4.setStyleSheet(self.defaultStyleSheet)
    recorderOutputFormLayout.addRow(self.QFormLayoutLeftLabel4, self.timeLabel)   
        
    self.snrLabel = qt.QLabel('-')
    self.snrLabel.setStyleSheet(self.defaultStyleSheet)
    self.QFormLayoutLeftLabel5 = qt.QLabel('SNR (%): ')
    self.QFormLayoutLeftLabel5.setStyleSheet(self.defaultStyleSheet)
    recorderOutputFormLayout.addRow(self.QFormLayoutLeftLabel5, self.snrLabel)    
    
    self.totalLabel = qt.QLabel('-')
    self.totalLabel.setStyleSheet(self.defaultStyleSheet)
    self.QFormLayoutLeftLabel6 = qt.QLabel('Total: ')
    self.QFormLayoutLeftLabel6.setStyleSheet(self.defaultStyleSheet)
    recorderOutputFormLayout.addRow(self.QFormLayoutLeftLabel6, self.totalLabel)    
    
    dummyLabel2 = qt.QLabel('')
    recorderOutputFormLayout.addRow('', dummyLabel2)
    
    self.infoLabel = qt.QLabel('Make sure Plus is running')
    self.infoLabel.setWordWrap(True)
    self.infoLabel.setStyleSheet(self.errorStyleSheet)
    self.QFormLayoutLeftLabel7 = qt.QLabel('INFO: ')
    self.QFormLayoutLeftLabel7.setStyleSheet(self.defaultStyleSheet)
    recorderOutputFormLayout.addRow(self.QFormLayoutLeftLabel7, self.infoLabel)

    # Live Filtering
    self.recorderFilteringGroupBox = ctk.ctkCollapsibleGroupBox()
    self.recorderFilteringGroupBox.setTitle("Live Filtering")
    recorderFilteringFormLayout = qt.QFormLayout(self.recorderFilteringGroupBox)
    recorderFormLayout.addRow(self.recorderFilteringGroupBox)
    
    self.snrFilteringSlider = ctk.ctkSliderWidget()
    self.snrFilteringSlider.setDecimals(0)
    self.snrFilteringSlider.singleStep = 1
    self.snrFilteringSlider.minimum = 0
    self.snrFilteringSlider.maximum = 100
    self.snrFilteringSlider.value = 40
    recorderFilteringFormLayout.addRow('SNR (%): ', self.snrFilteringSlider)
    
    self.distanceFilteringSlider = ctk.ctkRangeWidget()
    self.distanceFilteringSlider.minimum = 0
    self.distanceFilteringSlider.maximum = 500
    self.distanceFilteringSlider.setValues(0, 500)
    recorderFilteringFormLayout.addRow('Distance (mm): ', self.distanceFilteringSlider)
    
    # Intuitive Colouring
    self.colouringGroupBox = ctk.ctkCollapsibleGroupBox()
    self.colouringGroupBox.setTitle("Intuitive Colouring")
    colouringFormLayout = qt.QFormLayout(self.colouringGroupBox)
    recorderFormLayout.addRow(self.colouringGroupBox)
    
    hBoxLayoutColouring = qt.QHBoxLayout()
    colouringFormLayout.addRow(hBoxLayoutColouring)
    
    self.rasLabel = qt.QLabel('Direction: ')
    hBoxLayoutColouring.addWidget(self.rasLabel)
    self.rasComboBox = qt.QComboBox()
    self.rasComboBox.addItem('R')  
    self.rasComboBox.addItem('A')
    self.rasComboBox.addItem('S')               
    hBoxLayoutColouring.addWidget(self.rasComboBox)     
    
    self.minLabel = qt.QLabel('    Minimum: ')
    hBoxLayoutColouring.addWidget(self.minLabel)
    self.minSpinBox = qt.QDoubleSpinBox ()
    self.minSpinBox.setMinimum(-500)
    self.minSpinBox.setMaximum(500)
    self.minSpinBox.setSingleStep(0.1)
    self.minSpinBox.setValue(0.0)
    hBoxLayoutColouring.addWidget(self.minSpinBox)    
    
    self.maxLabel = qt.QLabel('    Maximum: ')
    hBoxLayoutColouring.addWidget(self.maxLabel)
    self.maxSpinBox = qt.QDoubleSpinBox ()
    self.maxSpinBox.setMinimum(-500)
    self.maxSpinBox.setMaximum(500)
    self.maxSpinBox.setSingleStep(0.1)
    self.maxSpinBox.setValue(0.0)
    hBoxLayoutColouring.addWidget(self.maxSpinBox)

    hBoxLayoutColouring.addStretch()
      
    # Controls
    self.controlsGroupBox = ctk.ctkCollapsibleGroupBox()
    self.controlsGroupBox.setTitle("Controls")
    controlsFormLayout = qt.QFormLayout(self.controlsGroupBox)
    recorderFormLayout.addRow(self.controlsGroupBox)
    
    hBoxLayoutControls = qt.QHBoxLayout()
    controlsFormLayout.addRow(hBoxLayoutControls)

    self.initButton = qt.QPushButton(" Init")
    self.initButton.setIcon(self.playIcon)
    self.initButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.initButton.enabled = True
    hBoxLayoutControls.addWidget(self.initButton)

    self.recordButton = qt.QPushButton(" Record")
    self.recordButton.setIcon(self.recordIcon)
    self.recordButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.recordButton.enabled = False
    self.recordButton.checkable = True
    hBoxLayoutControls.addWidget(self.recordButton)
    
    self.probeDialogButton = qt.QPushButton("ProbeDialog")
    self.probeDialogButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.probeDialogButton.enabled = False
    hBoxLayoutControls.addWidget(self.probeDialogButton)    

    self.saveButton = qt.QPushButton(" Save")
    self.saveButton.setIcon(self.saveIcon)
    self.saveButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.saveButton.enabled = False
    hBoxLayoutControls.addWidget(self.saveButton)
    
    self.resetButton = qt.QPushButton(" Reset")
    self.resetButton.setIcon(self.restartIcon)
    self.resetButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.resetButton.enabled = False
    hBoxLayoutControls.addWidget(self.resetButton)
    
    hBoxCheckBoxes = qt.QHBoxLayout()
    controlsFormLayout.addRow(hBoxCheckBoxes)

    self.viewpointCheckBox = qt.QCheckBox('Enable Viewpoint')
    self.viewpointCheckBox.checked = True
    self.viewpointCheckBox.enabled = False
    hBoxCheckBoxes.addWidget(self.viewpointCheckBox) 

    self.singlePointCheckBox = qt.QCheckBox('Single Measurements')
    self.singlePointCheckBox.checked = False
    self.singlePointCheckBox.enabled = False
    hBoxCheckBoxes.addWidget(self.singlePointCheckBox) 
    
    self.plusRemoteCheckBox = qt.QCheckBox('Record PLUS Data Stream')
    self.plusRemoteCheckBox.checked = False
    self.plusRemoteCheckBox.enabled = False
    hBoxCheckBoxes.addWidget(self.plusRemoteCheckBox)    
    
    # Post-Processing
    self.postProcessingGroupBox = ctk.ctkCollapsibleGroupBox()
    self.postProcessingGroupBox.setTitle("Post-Processing")
    postProcessingFormLayout = qt.QFormLayout(self.postProcessingGroupBox)
    recorderFormLayout.addRow(self.postProcessingGroupBox)    
    
    self.snrPostProcessingSlider = ctk.ctkSliderWidget()
    self.snrPostProcessingSlider.setDecimals(0)
    self.snrPostProcessingSlider.singleStep = 1
    self.snrPostProcessingSlider.minimum = 0
    self.snrPostProcessingSlider.maximum = 100
    self.snrPostProcessingSlider.value = 0
    postProcessingFormLayout.addRow('SNR (%): ', self.snrPostProcessingSlider)
    
    self.distancePostProcessingSlider = ctk.ctkRangeWidget()
    self.distancePostProcessingSlider.minimum = 0
    self.distancePostProcessingSlider.maximum = 500
    self.distancePostProcessingSlider.setValues(0, 500)
    postProcessingFormLayout.addRow('Distance (mm): ', self.distancePostProcessingSlider)
    
    hBoxLayoutPostProcessing = qt.QHBoxLayout()
    postProcessingFormLayout.addRow(hBoxLayoutPostProcessing)

    self.undoButton = qt.QPushButton("Undo")
    self.undoButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.undoButton.enabled = False
    hBoxLayoutPostProcessing.addWidget(self.undoButton)

    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
    self.applyButton.enabled = False
    hBoxLayoutPostProcessing.addWidget(self.applyButton)
    
    ######################################################## Connections
    self.snrFilteringSlider.connect('valueChanged(double)', self.onSnrFilteringValueChanged)
    self.distanceFilteringSlider.connect('maximumValueChanged(double)', self.onDistanceFilteringMaximumValueChanged)
    self.distanceFilteringSlider.connect('minimumValueChanged(double)', self.onDistanceFilteringMinimumValueChanged)
    self.initButton.connect('clicked(bool)', self.onInitClicked)
    self.recordButton.connect('clicked(bool)', self.onRecordClicked)
    self.resetButton.connect('clicked(bool)', self.onResetClicked)
    self.probeDialogButton.connect('clicked(bool)', self.onProbeDialogClicked)
    self.saveButton.connect('clicked(bool)', self.onSaveClicked)
    self.undoButton.connect('clicked(bool)', self.onUndoClicked)
    self.applyButton.connect('clicked(bool)', self.onApplyClicked)
    self.viewpointCheckBox.connect('stateChanged(int)', self.onViewpointChecked)
    self.plusRemoteCheckBox.connect('stateChanged(int)', self.onPlusRemoteChecked)
    
    # Add vertical spacer
    self.layout.addStretch(1) 
       
    # Create Plus connector and activate it
    self.conoProbeConnectorLogic.setupPlus()

  def onPlusRemoteChecked(self, checked):
    if checked:      
      self.conoProbeConnectorLogic.plusStartRecording()
    else:      
      self.conoProbeConnectorLogic.plusStopRecording()
    
  def onViewpointChecked(self, checked):
    if checked:
      self.conoProbeConnectorLogic.startViewpoint()
    else:
      self.conoProbeConnectorLogic.stopViewpoint()
  
  def onApplyClicked(self):
    self.conoProbeConnectorLogic.performPostProcessing(self.snrPostProcessingSlider.value, self.distancePostProcessingSlider.minimum, self.distancePostProcessingSlider.maximum)

  def onUndoClicked(self):
    self.conoProbeConnectorLogic.undoPostProcessing()
  
  def onSnrFilteringValueChanged(self, value):
    self.conoProbeConnectorLogic.snrThreshold = value 
    
  def onDistanceFilteringMaximumValueChanged(self, value):
    self.conoProbeConnectorLogic.distanceMaximumValue = value 
    
  def onDistanceFilteringMinimumValueChanged(self, value):
    self.conoProbeConnectorLogic.distanceMinimumValue = value 
  
  def onSaveClicked(self):
    self.conoProbeConnectorLogic.saveData()
  
  def onInitClicked(self):   
    labels = [self.distanceLabel, 
              self.snrLabel, 
              self.totalLabel, 
              self.infoLabel, 
              self.positionLabel, 
              self.nbrOfPointsRecordedLabel,
              self.timeLabel, 
              self.powerLabel, 
              self.frequencyLabel,
              self.lensMaxLabel,
              self.lensMinLabel]       
    self.conoProbeConnectorLogic.setOutPutLabels(labels)    

    # Create transform tree
    if not self.conoProbeConnectorLogic.createTransformTree():
      return
    
    # Add StopWatch
    self.conoProbeConnectorLogic.addStopWatch()
    
    # Add observer to parameters transform
    self.conoProbeConnectorLogic.addUpdateObserver()
    
    # Setup ViewpointLogic
    if self.viewpointCheckBox.checked:
      self.conoProbeConnectorLogic.initViewpoint()
    
    # Set layout (three 3D views w. different focal axes)
    self.conoProbeConnectorLogic.setLayout()   
    
    # Set min and max threshold to lens min and max
    minMax = self.conoProbeConnectorLogic.getLensMinMax()    
    self.distanceFilteringSlider.setValues(minMax[0], minMax[1])    
    self.onDistanceFilteringMinimumValueChanged(minMax[0])
    self.onDistanceFilteringMaximumValueChanged(minMax[1])
        
    self.initButton.enabled = False
    self.recordButton.enabled = True
    self.resetButton.enabled = True
    self.probeDialogButton.enabled = True
    self.viewpointCheckBox.enabled = True
    self.plusRemoteCheckBox.enabled = True
    self.singlePointCheckBox.enabled = True
    
  def onRecordClicked(self):    
    if self.singlePointCheckBox.checked:
      self.conoProbeConnectorLogic.acquireSingleMeasurement()
      self.recordButton.checked = False
      return    
    if self.recordButton.checked:
      if self.conoProbeConnectorLogic.direction == -1 and self.firstInitColouring:   
        self.conoProbeConnectorLogic.initColouring(self.rasComboBox.currentIndex, self.minSpinBox.value, self.maxSpinBox.value)
        self.firstInitColouring = False
      self.conoProbeConnectorLogic.stopWatch.start()
      self.conoProbeConnectorLogic.record = True
      self.enableWidgets(False)
    elif not self.recordButton.checked:
      self.conoProbeConnectorLogic.stopWatch.pause()
      self.conoProbeConnectorLogic.record = False
      self.conoProbeConnectorLogic.saveRecordedDataToDefault()
      self.enableWidgets(True)
    
  def onResetClicked(self):
    reply = qt.QMessageBox.question(slicer.util.mainWindow(), 'Reset recorded points', 'Are you sure you want to reset?', qt.QMessageBox.Yes, qt.QMessageBox.No)
    if reply == qt.QMessageBox.Yes:
      self.conoProbeConnectorLogic.stopWatch.reset()
      self.conoProbeConnectorLogic.reset = True
      self.saveButton.enabled = False    
      self.applyButton.enabled = False
      self.undoButton.enabled = False 
      if self.minSpinBox.value != self.maxSpinBox.value:
        if self.conoProbeConnectorLogic.direction == -1:   
          self.conoProbeConnectorLogic.initColouring(self.rasComboBox.currentIndex, self.minSpinBox.value, self.maxSpinBox.value)
        self.firstInitColouring = True
      if self.conoProbeConnectorLogic.direction > -1:   
        self.conoProbeConnectorLogic.initColouring(self.rasComboBox.currentIndex, self.minSpinBox.value, self.maxSpinBox.value)      
      if self.plusRemoteCheckBox.checked:
        self.onPlusRemoteChecked(False)
        self.plusRemoteCheckBox.checked = False
    else:
      return    
               
  def onProbeDialogClicked(self):
    self.conoProbeConnectorLogic.openProbeDialog()
    
  def enableWidgets(self, enable):
    self.saveButton.enabled = enable
    self.applyButton.enabled = enable
    self.undoButton.enabled = enable    
    self.singlePointCheckBox.enabled = enable
  
######################################################## ConoProbeConnectorLogic
class ConoProbeConnectorLogic(ScriptedLoadableModuleLogic):

  def __init__(self):  
    # Member variables
    self.outputLabels = None    
    self.recordedDataBuffer = []   
    self.record = False
    self.reset = False
    self.outputObserverTag = -1
    self.rigidBodyToTrackerTransformNode = None
    self.measurementToMeasurerTransformNode = None
    self.parametersToMeasurerTransformNode = None
    self.plus = None
    self.m = vtk.vtkMatrix4x4()
    self.direction = -1
    self.ras = [0, 0, 0, 1]
    self.d = 0.0
    self.snr = 0
    self.total = 0
    self.LABEL_UPDATE_RATE = 10  
    self.labelUpdateCount = 0
    self.snrThreshold = 40       
    self.distanceMaximumValue = 1000.0       
    self.distanceMinimumValue = 0.0 
    self.lensMaxDistance = 0.0
    self.lensMinDistance = 0.0
    self.normalizingConstant = 0.0
    self.min = -1000.0
    self.addColours = True
    import Viewpoint # Viewpoint
    self.viewpointLogic = Viewpoint.ViewpointLogic()
    self.stopWatch = None # StopWatch        
    # Create style sheets        
    self.errorStyleSheet = "QLabel { color : #FF0000; \
                                font: bold 14px}"
    self.defaultStyleSheet = "QLabel { color : #000000; \
                                  font: bold 14px}"        
    # Create rainbow colour table                                      
    self.colorTable=slicer.vtkMRMLColorTableNode()
    self.colorTable.SetTypeToRainbow ()                                    
    # Add MeasurementPoint
    self.measurementPointMarkupsFiducialNode = slicer.util.getNode('MeasurementPoint')
    if not self.measurementPointMarkupsFiducialNode:
      self.measurementPointMarkupsFiducialNode = slicer.vtkMRMLMarkupsFiducialNode()  
      self.measurementPointMarkupsFiducialNode.SetName('MeasurementPoint')
      self.measurementPointMarkupsFiducialNode.AddFiducial(0, 0, 0)
      self.measurementPointMarkupsFiducialNode.SetNthFiducialLabel(0, '')
      slicer.mrmlScene.AddNode(self.measurementPointMarkupsFiducialNode)
      self.measurementPointMarkupsFiducialNode.GetDisplayNode().SetGlyphScale(2.0)
      self.measurementPointMarkupsFiducialNode.GetDisplayNode().SetGlyphType(13) # Sphere3D
      self.measurementPointMarkupsFiducialNode.GetDisplayNode().SetSelectedColor(1, 0, 0)     
    # Add RecordedModel
    self.recordedModelNode = slicer.util.getNode('RecordedModel')
    if not self.recordedModelNode:
      recordedPoints = vtk.vtkPoints()
      recordedVertices = vtk.vtkCellArray()               
      recordedPolyData = vtk.vtkPolyData()
      recordedPolyData.SetPoints(recordedPoints)
      recordedPolyData.SetVerts(recordedVertices)
      self.recordedModelNode = self.addModelToScene(recordedPolyData, "RecordedModel")    
      self.recordedModelNode.GetModelDisplayNode().SetPointSize(3)
      # Set up coloured scalars  
      colorArray = vtk.vtkDoubleArray()
      colorArray.SetNumberOfComponents(4)
      colorArray.SetName('Colors')
      self.recordedModelNode.GetPolyData().GetPointData().SetScalars(colorArray)          
    # Create share directory
    self.pathToCreatedSaveDir = self.createShareDirectory()    
    # Post-Processing default (for undo)
    self.recordedDataBufferDefault = []
    
  def __del__(self):
    self.removeUpdateObserver()
    self.viewpointLogic.stopViewpoint()
  
  def initColouring(self, direction, min, max):
    if max > min:
      newMin = 0
      newMax = 255
      self.min = min
      self.direction = direction
      self.normalizingConstant = (newMax - newMin) / (max - min)
      return True
    else:
      logging.warning('Not possible to enable Intuitive Colouring: max <= min')
      return False
  
  def addStopWatch(self):
    from libs.StopWatch import StopWatch 
    self.stopWatch = StopWatch()
  
  def startViewpoint(self):
    self.viewpointLogic.startViewpoint()
  
  def stopViewpoint(self):
    self.viewpointLogic.stopViewpoint()
    
  def initViewpoint(self):
    if self.rigidBodyToTrackerTransformNode:
      # ConoProbeModelToMeasurement
      conoProbeModelToMeasurement = slicer.util.getNode('ConoProbeModelToMeasurement')      
      if not conoProbeModelToMeasurement:
        conoProbeModelToMeasurement=slicer.vtkMRMLLinearTransformNode()
        conoProbeModelToMeasurement.SetName("ConoProbeModelToMeasurement")
        m = vtk.vtkMatrix4x4()
        # Large lens
        # m.SetElement( 0, 0, -0.92 ) # Row 1
        # m.SetElement( 0, 1, -0.16 )
        # m.SetElement( 0, 2, 0.37 )
        # m.SetElement( 0, 3, 63.53 )      
        # m.SetElement( 1, 0, -0.38 )  # Row 2
        # m.SetElement( 1, 1, 0.06 )
        # m.SetElement( 1, 2, -0.92 )
        # m.SetElement( 1, 3, 81.99 )       
        # m.SetElement( 2, 0, 0.13 )  # Row 3
        # m.SetElement( 2, 1, -0.98 )
        # m.SetElement( 2, 2, -0.12 )
        # m.SetElement( 2, 3, -40.15 )
        # Small lens
        m.SetElement( 0, 0, -0.92 ) # Row 1
        m.SetElement( 0, 1, -0.16 )
        m.SetElement( 0, 2, 0.37 )
        m.SetElement( 0, 3, 63.53 )      
        m.SetElement( 1, 0, -0.38 )  # Row 2
        m.SetElement( 1, 1, 0.06 )
        m.SetElement( 1, 2, -0.92 )
        m.SetElement( 1, 3, 81.99 )       
        m.SetElement( 2, 0, 0.13 )  # Row 3
        m.SetElement( 2, 1, -0.98 )
        m.SetElement( 2, 2, -0.12 )
        m.SetElement( 2, 3, 129.85 )
        conoProbeModelToMeasurement.SetMatrixTransformToParent(m)
        slicer.mrmlScene.AddNode(conoProbeModelToMeasurement)
      conoProbeModelToMeasurement.SetAndObserveTransformNodeID(self.rigidBodyToTrackerTransformNode.GetID())    
      # ViewPointToMeasurement
      viewPointToMeasurement = slicer.util.getNode('ViewPointToMeasurement')
      if not viewPointToMeasurement:
        viewPointToMeasurement=slicer.vtkMRMLLinearTransformNode()
        viewPointToMeasurement.SetName("ViewPointToMeasurement")
        m = vtk.vtkMatrix4x4()
        # Large lens
        # m.SetElement( 0, 0, -1 ) # Row 1
        # m.SetElement( 0, 1, 0 )
        # m.SetElement( 0, 2, 0 )
        # m.SetElement( 0, 3, 53.00 )      
        # m.SetElement( 1, 0, 0 )  # Row 2
        # m.SetElement( 1, 1, -1 )
        # m.SetElement( 1, 2, 0 )
        # m.SetElement( 1, 3, 88.00 )       
        # m.SetElement( 2, 0, 0 )  # Row 3
        # m.SetElement( 2, 1, 0 )
        # m.SetElement( 2, 2, 1 )
        # m.SetElement( 2, 3, -106 )
        # Small lens
        m.SetElement( 0, 0, -1 ) # Row 1
        m.SetElement( 0, 1, 0 )
        m.SetElement( 0, 2, 0 )
        m.SetElement( 0, 3, 53.00 )      
        m.SetElement( 1, 0, 0 )  # Row 2
        m.SetElement( 1, 1, -1 )
        m.SetElement( 1, 2, 0 )
        m.SetElement( 1, 3, 88.00 )       
        m.SetElement( 2, 0, 0 )  # Row 3
        m.SetElement( 2, 1, 0 )
        m.SetElement( 2, 2, 1 )
        m.SetElement( 2, 3, 54 )
        viewPointToMeasurement.SetMatrixTransformToParent(m)
        slicer.mrmlScene.AddNode(viewPointToMeasurement)
      viewPointToMeasurement.SetAndObserveTransformNodeID(self.rigidBodyToTrackerTransformNode.GetID())  
      # ConoProbeModel
      conoProbeModel = slicer.util.getNode('ConoProbeModel')
      if not conoProbeModel:
        moduleDirectoryPath = slicer.modules.conoprobeconnector.path.replace('ConoProbeConnector.py', '')
        slicer.util.loadModel(qt.QDir.toNativeSeparators(moduleDirectoryPath + '../../Data/Models/ConoProbeModel.stl'))
        conoProbeModel=slicer.util.getNode(pattern="ConoProbeModel")
        conoProbeModel.SetName("ConoProbeModel")   
        conoProbeModel.GetDisplayNode().SetOpacity(0.7)
      conoProbeModel.SetAndObserveTransformNodeID(conoProbeModelToMeasurement.GetID())      
      # Camera
      camera = slicer.util.getNode('Camera')
      if not camera:
        camera=slicer.vtkMRMLCameraNode()
        camera.SetName("Camera")
        slicer.mrmlScene.AddNode(camera)
      threeDView = slicer.util.getNode("view1")
      camera.SetActiveTag(threeDView.GetID())        
      # Viewpoint
      self.viewpointLogic.setCameraNode(camera)
      self.viewpointLogic.setTransformNode(viewPointToMeasurement)
      self.viewpointLogic.setModelPOVOnNode(conoProbeModel)
      self.viewpointLogic.SetCameraXPosMm(53)
      self.viewpointLogic.SetCameraYPosMm(72)
      self.viewpointLogic.SetCameraZPosMm(119)
      self.viewpointLogic.startViewpoint()

  def getLensMinMax(self):
    minMax = [0, 0]
    self.parametersToMeasurerTransformNode.GetMatrixTransformToParent(self.m)    
    minMax[0] = self.m.GetElement(2, 0)     
    minMax[1] = self.m.GetElement(2, 1)   
    return minMax

  def saveRecordedDataToDefault(self):    
    self.recordedDataBufferDefault = self.recordedDataBuffer 
    
  def performPostProcessing(self, snrThreshold, distanceMinimumValue, distanceMaximumValue): 
    # Create new vtkPolyData
    newPoints = vtk.vtkPoints()
    newVertices = vtk.vtkCellArray()               
    newPolyData = vtk.vtkPolyData()
    newPolyData.SetPoints(newPoints)
    newPolyData.SetVerts(newVertices)
    colorArray = vtk.vtkDoubleArray()
    colorArray.SetNumberOfComponents(4)
    colorArray.SetName('Colors')
    newPolyData.GetPointData().SetScalars(colorArray)   
    # Filter accordingly to the input parameters
    recordedDataBufferFiltered = []    
    for idx in range(len(self.recordedDataBuffer)):
      d = self.recordedDataBuffer[idx][3]
      snr = self.recordedDataBuffer[idx][4]
      if (snr > snrThreshold and
          d < distanceMaximumValue and       
          d > distanceMinimumValue):
          recordedDataBufferFiltered.append(self.recordedDataBuffer[idx])   
          self.addPointToPolyData(newPolyData, self.recordedDataBuffer[idx][0:3])
    # Update recorded model and buffer
    self.recordedModelNode.GetPolyData().DeepCopy(newPolyData)     
    self.recordedModelNode.GetPolyData().Modified()  
    self.recordedDataBuffer = recordedDataBufferFiltered
    
  def showColouring(self):
    self.recordedModelNode.GetModelDisplayNode().SetActiveScalarName('Colors')
    self.recordedModelNode.GetModelDisplayNode().SetScalarVisibility(True)  
    
  def undoPostProcessing(self):
    # Create new vtkPolyData
    newPoints = vtk.vtkPoints()
    newVertices = vtk.vtkCellArray()               
    newPolyData = vtk.vtkPolyData()
    newPolyData.SetPoints(newPoints)
    newPolyData.SetVerts(newVertices)
    colorArray = vtk.vtkDoubleArray()
    colorArray.SetNumberOfComponents(4)
    colorArray.SetName('Colors')
    newPolyData.GetPointData().SetScalars(colorArray)   
    # Filter accordingly to the input parameters
    recordedDataBufferFiltered = []    
    for idx in range(len(self.recordedDataBufferDefault)):
      self.addPointToPolyData(newPolyData, self.recordedDataBufferDefault[idx][0:3])
    # Update recorded model and buffer
    self.recordedModelNode.GetPolyData().DeepCopy(newPolyData)     
    self.recordedModelNode.GetPolyData().Modified()  
    self.recordedDataBuffer = self.recordedDataBufferDefault
    
  def setOutPutLabels(self, labels):
    self.outputLabels = labels
    
  def saveData(self):
    dateAndTime = time.strftime("_%Y-%m-%d_%H-%M-%S")  
    path = self.pathToCreatedSaveDir + '/Points' + dateAndTime  
    # Save model to .vtk
    slicer.modules.models.logic().SaveModel(path + '.vtk', self.recordedModelNode)
    # Save data to .csv 
    self.writeRecordedDataBufferToFile(path + '.csv')  
    saveDir = self.pathToCreatedSaveDir.split('SlicerModules')[1] # Just to remove unnecessary information
    self.outputLabels[3].setText('Data saved to: ' + saveDir)
    
  def writeRecordedDataBufferToFile(self, path): 
    with open(path, 'wb') as csvfile:
      writer = csv.writer(csvfile, delimiter=",")
      writer.writerow(['x_ConoProbe', 'y_ConoProbe', 'z_ConoProbe', 'd', 'snr', 'total', 'x_RigidBody', 'y_RigidBody', 'z_RigidBody', 'Rxx', 'Rxy', 'Rxz', 'Ryx', 'Ryy', 'Ryz', 'Rzx', 'Rzy', 'Rzz'])
      for idx in range(len(self.recordedDataBuffer)):       
        writer.writerow(self.recordedDataBuffer[idx])
  
  def getModelXYZ(self):
    xyz = []
    for idx in range(self.recordedModelNode.GetPolyData().GetPoints().GetNumberOfPoints()):
      point = [0, 0, 0]
      self.recordedModelNode.GetPolyData().GetPoint(idx, point)
      xyz.append(point)      
    return xyz
  
  def createShareDirectory(self): 
    date = time.strftime("%Y-%m-%d")        
    shareDirPath = slicer.modules.conoprobeconnector.path.replace("ConoProbeConnector.py","") + 'Output/' + date
    if not os.path.exists(shareDirPath):
      os.makedirs(shareDirPath)   
    return shareDirPath
    
  def addModelToScene(self, polyData, name):
    scene = slicer.mrmlScene
    node = slicer.vtkMRMLModelNode()
    node.SetScene(scene)
    node.SetName(name)
    node.SetAndObservePolyData(polyData)
    modelDisplay = slicer.vtkMRMLModelDisplayNode()
    modelDisplay.SetColor(0, 1, 0)
    modelDisplay.SetScene(scene)
    scene.AddNode(modelDisplay)
    node.SetAndObserveDisplayNodeID(modelDisplay.GetID())
    scene.AddNode(node)
    return node
  
  def clearPointsInRecordedModel(self): 
    self.recordedDataBuffer = [] 
    newPoints = vtk.vtkPoints()
    newVertices = vtk.vtkCellArray()               
    newPolyData = vtk.vtkPolyData()
    newPolyData.SetPoints(newPoints)
    newPolyData.SetVerts(newVertices)
    colorArray = vtk.vtkDoubleArray()
    colorArray.SetNumberOfComponents(4)
    colorArray.SetName('Colors')
    newPolyData.GetPointData().SetScalars(colorArray)   
    self.recordedModelNode.GetPolyData().DeepCopy(newPolyData)     
    self.recordedModelNode.GetPolyData().Modified()        
      
  def setupPlus(self):
    connectorNode = self.createPlusConnector()
    connectorNode.Start()      
    self.plus = Plus(connectorNode.GetID(), self.pathToCreatedSaveDir)
  
  def plusStartRecording(self):
    dateAndTime = time.strftime("_%Y-%m-%d_%H-%M-%S")
    self.plus.startStopRecording(True, 'PlusRecording' + dateAndTime + '.mha')

  def plusStopRecording(self):    
    self.plus.startStopRecording(False)
    
  def createTransformTree(self):
    # Get transform nodes from scene
    if not self.rigidBodyToTrackerTransformNode:
      self.rigidBodyToTrackerTransformNode = slicer.util.getNode('RigidBodyToTracker')
    if not self.measurementToMeasurerTransformNode:
      self.measurementToMeasurerTransformNode = slicer.util.getNode('MeasurementToMeasure')
    if not self.parametersToMeasurerTransformNode:
      self.parametersToMeasurerTransformNode = slicer.util.getNode('ParametersToMeasurer')
    if not self.measurementToMeasurerTransformNode or not self.parametersToMeasurerTransformNode:
      logging.error('Missing transform! Is Plus properly configured?')
      self.outputLabels[3].setText('Missing transform! Is PlusServer running and properly configured?')
      self.outputLabels[3].setStyleSheet(self.errorStyleSheet)
      return False
    if not self.rigidBodyToTrackerTransformNode:
      logging.warning('No tracking transform present, only raw measurement.')      
    self.outputLabels[3].setText(' ')
    self.outputLabels[3].setStyleSheet(self.defaultStyleSheet)       
    if self.measurementToMeasurerTransformNode:
      self.measurementPointMarkupsFiducialNode.SetAndObserveTransformNodeID(self.measurementToMeasurerTransformNode.GetID())
    if self.rigidBodyToTrackerTransformNode:
      self.measurementToMeasurerTransformNode.SetAndObserveTransformNodeID(self.rigidBodyToTrackerTransformNode.GetID())
    else:
      self.outputLabels[3].setText('No tracking transform present, only raw measurement.')
    return True
    
  # From: SlicerIGT/GuideletLib
  # Takes for granted IP:port is localhost:18944
  def createPlusConnector(self):
    connectorNode = slicer.util.getNode('PlusConnector')
    if not connectorNode:
      connectorNode = slicer.vtkMRMLIGTLConnectorNode()
      slicer.mrmlScene.AddNode(connectorNode)
      connectorNode.SetName('PlusConnector')      
      hostNamePort = "localhost:18944"
      [hostName, port] = hostNamePort.split(':')
      connectorNode.SetTypeClient(hostName, int(port))
      logging.debug("PlusConnector created")
    return connectorNode
    
  def addUpdateObserver(self):
    if self.outputObserverTag == -1:
      self.outputObserverTag = self.rigidBodyToTrackerTransformNode.AddObserver('ModifiedEvent', self.updateSceneCallback)
      logging.info('addOutputObserver')

  def removeUpdateObserver(self):
    if self.outputObserverTag != -1:
      self.parametersToMeasurerTransformNode.RemoveObserver(self.outputObserverTag)
      self.outputObserverTag = -1
      logging.info('removeOutputObserver')
  
  def updateSceneCallback(self, modifiedNode, event=None):                    
    # This lowers the update rate of the labels to only every self.LABEL_UPDATE_RATE measurement
    self.labelUpdateCount = self.labelUpdateCount + 1
    updateLabels = not self.labelUpdateCount % self.LABEL_UPDATE_RATE 
    if self.reset:
      self.clearPointsInRecordedModel()
      self.reset = False
    if updateLabels or self.record:
      # Get ConoProbe parameters
      self.parametersToMeasurerTransformNode.GetMatrixTransformToParent(self.m)
      self.d = self.m.GetElement(0, 0)
      self.snr = self.m.GetElement(0, 1)
      self.total = self.m.GetElement(0, 2)       
      self.power = self.m.GetElement(1, 1)
      self.frequency = self.m.GetElement(1, 0)   
      self.lensMaxDistance = self.m.GetElement(2, 0)   
      self.lensMinDistance = self.m.GetElement(2, 1)   
      # Get measurement coordinate
      self.measurementPointMarkupsFiducialNode.GetNthFiducialWorldCoordinates(0, self.ras)      
    if updateLabels:
      # Update output labels
      self.updateOutputLabels()      
      self.labelUpdateCount = 0
    if (self.record and self.snr > self.snrThreshold and self.d < self.distanceMaximumValue and self.d > self.distanceMinimumValue):
       self.acquireSingleMeasurement()
      
  def acquireSingleMeasurement(self):
    # Only for printing tracker position to file
    xRigidBodyToTracker = 0
    yRigidBodyToTracker = 0
    zRigidBodyToTracker = 0
    Rxx = 0
    Rxy = 0
    Rxz = 0
    Ryx = 0
    Ryy = 0
    Ryz = 0
    Rzx = 0
    Rzy = 0
    Rzz = 0
    if self.rigidBodyToTrackerTransformNode:
      self.rigidBodyToTrackerTransformNode.GetMatrixTransformToParent(self.m)
      xRigidBodyToTracker = self.m.GetElement(0, 3)
      yRigidBodyToTracker = self.m.GetElement(1, 3)
      zRigidBodyToTracker = self.m.GetElement(2, 3) 
      Rxx = self.m.GetElement(0, 0)
      Rxy = self.m.GetElement(0, 1)
      Rxz = self.m.GetElement(0, 2) 
      Ryx = self.m.GetElement(1, 0)
      Ryy = self.m.GetElement(1, 1)
      Ryz = self.m.GetElement(1, 2) 
      Rzx = self.m.GetElement(2, 0)
      Rzy = self.m.GetElement(2, 1)
      Rzz = self.m.GetElement(2, 2) 
    self.recordedDataBuffer.append([self.ras[0], self.ras[1], self.ras[2], 
                                    self.d, self.snr, self.total, 
                                    xRigidBodyToTracker, yRigidBodyToTracker, zRigidBodyToTracker,
                                    Rxx, Rxy, Rxz, Ryx, Ryy, Ryz, Rzx, Rzy, Rzz])      
    self.addPointToPolyData(self.recordedModelNode.GetPolyData(), self.ras)
  
  def updateOutputLabels(self):
    self.outputLabels[0].setText('%.1f' % self.d)
    self.outputLabels[1].setText('%.0f' % self.snr)
    self.outputLabels[2].setText('%.0f' % self.total)
    self.outputLabels[4].setText('[' + '%.1f' % self.ras[0] + ', ' + '%.1f' %  self.ras[1] + ', '+ '%.1f' %  self.ras[2] + ']')
    self.outputLabels[5].setText(str(self.recordedModelNode.GetPolyData().GetPoints().GetNumberOfPoints()))    
    self.outputLabels[6].setText('%.2f' % self.stopWatch.getElapsedTime())
    self.outputLabels[7].setText('%.0f' % self.power)
    self.outputLabels[8].setText('%.0f' % self.frequency)
    self.outputLabels[10].setText('%.1f' % self.lensMaxDistance)
    self.outputLabels[9].setText('%.1f' % self.lensMinDistance)
    
  def addPointToPolyData(self, polyData, ras):      
    pid = vtk.vtkIdList()
    pid.SetNumberOfIds(1);
    temp = polyData.GetPoints().InsertNextPoint(ras[0], ras[1], ras[2])    
    pid.SetId(0, temp)    
    polyData.GetVerts().InsertNextCell(pid)        
    if self.direction > -1:          
      color = [0, 0, 0, 0]  
      tableValue = 1 + (ras[self.direction] - self.min) * self.normalizingConstant
      if tableValue > 255:
        tableValue = 255
      elif tableValue < 0:
        tableValue = 0
      self.colorTable.GetColor(int(tableValue), color) # 0 -> 255
      self.recordedModelNode.GetPolyData().GetPointData().GetScalars('Colors').InsertTuple(self.recordedModelNode.GetPolyData().GetPoints().GetNumberOfPoints() - 1, color)
      if self.addColours:
        self.showColouring()
        self.addColours = False
    polyData.Modified() 
    
  def openProbeDialog(self):
    self.plus.showProbeDialog()
    
  def setLayout(self):
    lm=slicer.app.layoutManager()
    lm.setLayout(4) # One 3D-view
    self.resetLayoutFocalPoint(0)  
    self.zoomInThreeDView(0, 8)    
    self.setAxisAndBoxVisibility('View1', False)  
  
  def setAxisAndBoxVisibility(self, viewName, visible):
    view = slicer.mrmlScene.GetFirstNodeByName(viewName)               
    view.SetAxisLabelsVisible(visible)
    view.SetBoxVisible(visible)  
  
  def resetLayoutFocalPoint(self, viewIdx):
    threeDWidget = slicer.app.layoutManager().threeDWidget(viewIdx)
    threeDView = threeDWidget.threeDView()
    threeDView.resetFocalPoint()   
  
  def zoomInThreeDView(self, viewIdx, zoomFactor):
    threeDWidget = slicer.app.layoutManager().threeDWidget(viewIdx)
    threeDView = threeDWidget.threeDView()
    for zoom in range(zoomFactor):
      threeDView.zoomIn()
      
  # Available ctkAxes: 
  # - ctk.ctkAxesWidget.Right 
  # - ctk.ctkAxesWidget.Left
  # - ctk.ctkAxesWidget.Inferior
  # - ctk.ctkAxesWidget.Superior
  # - ctk.ctkAxesWidget.Posterior
  # - ctk.ctkAxesWidget.Anterior
  def setFocalPointByAxis(self, viewIdx, ctkAxis):
    view=slicer.app.layoutManager().threeDWidget(viewIdx).threeDView() 
    view.lookFromViewAxis(ctkAxis)

# For a future implementation in order to show the time live in the output    
class Timer(object):

  def __init__(self):
    self.startTime = 0.0
    self.stopTime = 0.0
    self.timerStarted = False
    
  def startTimer(self):
    if not self.timerStarted:      
      self.startTime = time.clock()
      if self.stopTime != 0.0:
        self.stopTime = time.clock() - self.stopTime
      self.timerStarted = True
    else:
      logging.warning('Timer already running')
      
  def stopTimer(self):
    if self.timerStarted:
      self.stopTime = time.clock()
      self.timerStarted = False
    else:
      logging.warning('Timer not running')
      
  def getElapsedTime(self):
    if self.startTime == 0.0:
      return 0.0
    elif self.stopTime == 0.0:
      return time.clock() - self.startTime
    else:
      return time.clock() - (self.stopTime - self.startTime)
        
  def resetTimer(self):
    if self.startTime != 0.0:
      self.startTime = time.clock()    
      self.stopTime = 0.0
  
class Plus(object):
  
  def __init__(self, connectorNodeID, shareDirPath):
    self.shareDirPath = shareDirPath   
    self.defaultCommandTimeoutSec = 30
    self.connectorNodeID = connectorNodeID 
    # Set commands
    self.cmdStartRecording = slicer.modulelogic.vtkSlicerOpenIGTLinkCommand()
    self.cmdStartRecording.SetCommandTimeoutSec(self.defaultCommandTimeoutSec);
    self.cmdStartRecording.SetCommandName('StartRecording')      
    self.cmdStopRecording = slicer.modulelogic.vtkSlicerOpenIGTLinkCommand()
    self.cmdStopRecording.SetCommandTimeoutSec(self.defaultCommandTimeoutSec);
    self.cmdStopRecording.SetCommandName('StopRecording') 
    self.cmdShowProbeDialog = slicer.modulelogic.vtkSlicerOpenIGTLinkCommand()
    self.cmdShowProbeDialog.SetCommandTimeoutSec(self.defaultCommandTimeoutSec);
    self.cmdShowProbeDialog.SetCommandName('ShowProbeDialog') 
    # Get remote logic
    self.remoteLogic = slicer.modules.openigtlinkremote.logic()
    if self.remoteLogic:
      self.remoteLogic.SetMRMLScene(slicer.mrmlScene)
    else:
      logging.error('Logic not found for OpenIGTRemote')
  
  def __del__(self):
    self.remoteLogic.SendCommand(self.cmdStopRecording, self.connectorNodeID)
  
  def showProbeDialog(self):
    if self.remoteLogic:
      self.remoteLogic.SendCommand(self.cmdShowProbeDialog, self.connectorNodeID)
  
  def startStopRecording(self, record, fileName="None"):  
    if self.remoteLogic:
      if record:
        self.cmdStartRecording.SetCommandAttribute('OutputFilename', self.shareDirPath + '/' + fileName)
        self.remoteLogic.SendCommand(self.cmdStartRecording, self.connectorNodeID)
        logging.debug('Start recording PLUS frames to ' + self.shareDirPath + '/' + fileName)
      elif not record:      
        self.remoteLogic.SendCommand(self.cmdStopRecording, self.connectorNodeID)
        logging.debug('Stop recording PLUS frames.')
      else:
        logging.warning('Could not record PLUS frames!')         
