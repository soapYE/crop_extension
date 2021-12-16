import os
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
#from matrix.py import get_rotation_matrix
import matrix

#
# crop
#

class crop(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "crop"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["Ziyu Li (uAlberta)","Yanquan Chen (uAlberta)","Fangyang Ye (uAlberta)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#crop">module documentation</a>.
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""

    # Additional initialization step after application startup is complete
    slicer.app.connect("startupCompleted()", registerSampleData)

#
# Register sample data sets in Sample Data module
#

def registerSampleData():
  """
  Add data sets to Sample Data module.
  """
  # It is always recommended to provide sample data for users to make it easy to try the module,
  # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

  import SampleData
  iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')

  # To ensure that the source code repository remains small (can be downloaded and installed quickly)
  # it is recommended to store data sets that are larger than a few MB in a Github release.

  # crop1
  SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='crop',
    sampleName='crop1',
    # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
    # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
    thumbnailFileName=os.path.join(iconsPath, 'crop1.png'),
    # Download URL and target file name
    uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
    fileNames='crop1.nrrd',
    # Checksum to ensure file integrity. Can be computed by this command:
    #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
    checksums = 'SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95',
    # This node name will be used when the data set is loaded
    nodeNames='crop1'
  )

  # crop2
  SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='crop',
    sampleName='crop2',
    thumbnailFileName=os.path.join(iconsPath, 'crop2.png'),
    # Download URL and target file name
    uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
    fileNames='crop2.nrrd',
    checksums = 'SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97',
    # This node name will be used when the data set is loaded
    nodeNames='crop2'
  )

#
# cropWidget
#

class cropWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False

  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/crop.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    uiWidget.setMRMLScene(slicer.mrmlScene)

    # Create logic class. Logic implements all computations that should be possible to run
    # in batch mode, without a graphical user interface.
    self.logic = cropLogic()

    # Connections

    # These connections ensure that we update parameter node when scene is closed
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

    # These connections ensure that whenever user changes some settings on the GUI, that is saved in the MRML scene
    # (in the selected parameter node).
    self.ui.annotationROISelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.transformNodeSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    #self.ui.imageThresholdSliderWidget.connect("valueChanged(double)", self.updateParameterNodeFromGUI)
    #self.ui.invertOutputCheckBox.connect("toggled(bool)", self.updateParameterNodeFromGUI)
    #self.ui.invertedOutputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.LRSlider.connect("valueChanged(double)",self.updateParameterNodeFromGUI)
    self.ui.PASlider.connect("valueChanged(double)",self.updateParameterNodeFromGUI)
    self.ui.ISSlider.connect("valueChanged(double)",self.updateParameterNodeFromGUI)

    # Buttons
    self.ui.showROICheckBox.connect('toggled(bool)', self.onCheckedShowROI)
    self.ui.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.ui.resetButton.connect("clicked(bool)", self.onResetButton)

    # Make sure parameter node is initialized (needed for module reload)
    self.initializeParameterNode()

  def cleanup(self):
    """
    Called when the application closes and the module widget is destroyed.
    """
    self.removeObservers()

  def enter(self):
    """
    Called each time the user opens this module.
    """
    # Make sure parameter node exists and observed
    self.initializeParameterNode()

  def exit(self):
    """
    Called each time the user opens a different module.
    """
    # Do not react to parameter node changes (GUI wlil be updated when the user enters into the module)
    self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

  def onSceneStartClose(self, caller, event):
    """
    Called just before the scene is closed.
    """
    # Parameter node will be reset, do not use it anymore
    self.setParameterNode(None)

  def onSceneEndClose(self, caller, event):
    """
    Called just after the scene is closed.
    """
    # If this module is shown while the scene is closed then recreate a new parameter node immediately
    if self.parent.isEntered:
      self.initializeParameterNode()

  def initializeParameterNode(self):
    """
    Ensure parameter node exists and observed.
    """
    # Parameter node stores all user choices in parameter values, node selections, etc.
    # so that when the scene is saved and reloaded, these settings are restored.

    self.setParameterNode(self.logic.getParameterNode())

    # Select default input nodes if nothing is selected yet to save a few clicks for the user
    if not self._parameterNode.GetNodeReference("InputVolume"):
      firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
      if firstVolumeNode:
        self._parameterNode.SetNodeReferenceID("InputVolume", firstVolumeNode.GetID())

  def setParameterNode(self, inputParameterNode):
    """
    Set and observe parameter node.
    Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
    """

    if inputParameterNode:
      self.logic.setDefaultParameters(inputParameterNode)

    # Unobserve previously selected parameter node and add an observer to the newly selected.
    # Changes of parameter node are observed so that whenever parameters are changed by a script or any other module
    # those are reflected immediately in the GUI.
    if self._parameterNode is not None:
      self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
    self._parameterNode = inputParameterNode
    if self._parameterNode is not None:
      self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

    # Initial GUI update
    self.updateGUIFromParameterNode()

  def updateGUIFromParameterNode(self, caller=None, event=None):
    """
    This method is called whenever parameter node is changed.
    The module GUI is updated to show the current state of the parameter node.
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    # Make sure GUI changes do not call updateParameterNodeFromGUI (it could cause infinite loop)
    print("gui changed!")
    self._updatingGUIFromParameterNode = True

    # Update node selectors and sliders
    self.ui.annotationROISelector.setCurrentNode(self._parameterNode.GetNodeReference("ROINode"))
    self.ui.inputSelector.setCurrentNode(self._parameterNode.GetNodeReference("InputVolume"))
    self.ui.transformNodeSelector.setCurrentNode(self._parameterNode.GetNodeReference("TransformNode"))
    self.ui.outputSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolume"))
    #self.ui.invertedOutputSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolumeInverse"))
    #self.ui.imageThresholdSliderWidget.value = float(self._parameterNode.GetParameter("Threshold"))
    #self.ui.invertOutputCheckBox.checked = (self._parameterNode.GetParameter("Invert") == "true")
    
    roi_node = self._parameterNode.GetNodeReference("ROINode")
    if roi_node:
      self.ui.showROICheckBox.checkable = True
      #print(self._parameterNode.GetNodeReference("ROINode").GetROIAnnotationVisibility())
      self.ui.showROICheckBox.checked = (self._parameterNode.GetNodeReference("ROINode").GetDisplayVisibility() == True)
    else:
      self.ui.showROICheckBox.checkable = False
    
    transform_node = self._parameterNode.GetNodeReference("TransformNode")
    if transform_node:
      self.ui.LRSlider.enabled = True
      self.ui.PASlider.enabled = True
      self.ui.ISSlider.enabled = True
      self.ui.resetButton.enabled = True
      # get transform_node's transform matrix, then calculate LR, PA, IS rotate degree. initialize the value
      #change to this matrix won't apply, see https://apidocs.slicer.org/master/classvtkMRMLTransformNode.html#aceaae1709642a781e6006fdc2578dc8c
      rotation_matrix = transform_node.GetMatrixTransformFromParent()
      LR, PA, IS = matrix.get_rotation_angle(rotation_matrix)
      print(PA)
      #set ui slider
      self.ui.LRSlider.value = LR
      self.ui.PASlider.value = PA
      self.ui.ISSlider.value = IS
      self._parameterNode.SetParameter("LR", str(self.ui.LRSlider.value))
      self._parameterNode.SetParameter("PA",str(self.ui.PASlider.value))
      self._parameterNode.SetParameter("IS",str(self.ui.ISSlider.value))
      '''
      if roi_node:
        roi_node.SetAndObserveTransformNodeID(transform_node.GetID())
      '''
    else:
      self.ui.LRSlider.enabled = False
      self.ui.PASlider.enabled = False
      self.ui.ISSlider.enabled = False
      self.ui.resetButton.enabled = False

    # Update buttons states and tooltips
    
    if roi_node and transform_node and self._parameterNode.GetNodeReference("OutputVolume"):
      self.ui.applyButton.enabled = True
    else:
      self.ui.applyButton.enabled = False

    self._updatingGUIFromParameterNode = False

  def updateParameterNodeFromGUI(self, caller=None, event=None):
    """
    This method is called when the user makes any change in the GUI.
    The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    print("parameter changed!")

    wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch


    self._parameterNode.SetNodeReferenceID("ROINode", self.ui.annotationROISelector.currentNodeID)
    self._parameterNode.SetNodeReferenceID("InputVolume", self.ui.inputSelector.currentNodeID)
    self._parameterNode.SetNodeReferenceID("TransformNode", self.ui.transformNodeSelector.currentNodeID)
    self._parameterNode.SetNodeReferenceID("OutputVolume", self.ui.outputSelector.currentNodeID)
    #self._parameterNode.SetParameter("Threshold", str(self.ui.imageThresholdSliderWidget.value))
    #self._parameterNode.SetParameter("Invert", "true" if self.ui.invertOutputCheckBox.checked else "false")
    #self._parameterNode.SetNodeReferenceID("OutputVolumeInverse", self.ui.invertedOutputSelector.currentNodeID)
    self._parameterNode.SetParameter("LR", str(self.ui.LRSlider.value))
    self._parameterNode.SetParameter("PA",str(self.ui.PASlider.value))
    self._parameterNode.SetParameter("IS",str(self.ui.ISSlider.value))

    LR = float(self._parameterNode.GetParameter("LR"))
    PA = float(self._parameterNode.GetParameter("PA"))
    IS = float(self._parameterNode.GetParameter("IS"))

    roi_node = self._parameterNode.GetNodeReference("ROINode")
    '''
    if roi_node:
      self.ui.showROICheckBox.checkable = True
      #print(self._parameterNode.GetNodeReference("ROINode").GetROIAnnotationVisibility())
      self.ui.showROICheckBox.checked = (self._parameterNode.GetNodeReference("ROINode").GetDisplayVisibility() == True)
    else:
      self.ui.showROICheckBox.checkable = False
    '''
    
    transform_node = self._parameterNode.GetNodeReference("TransformNode")
    if transform_node:
      rotation_matrix = matrix.get_rotation_matrix(LR,PA,IS)
      transform_node.SetMatrixTransformToParent(rotation_matrix)
      if roi_node:
        roi_node.SetAndObserveTransformNodeID(transform_node.GetID())
      '''
      self.ui.LRSlider.enabled = True
      self.ui.PASlider.enabled = True
      self.ui.ISSlider.enabled = True
      #compute rotation matrix and update transform node
      rotation_matrix = matrix.get_rotation_matrix(LR,PA,IS)
      transform_node.SetMatrixTransformToParent(rotation_matrix)
      if roi_node:
        roi_node.SetAndObserveTransformNodeID(transform_node.GetID())
    else:
      self.ui.LRSlider.enabled = True
      self.ui.PASlider.enabled = True
      self.ui.ISSlider.enabled = True
      '''
    

    self._parameterNode.EndModify(wasModified)

  def onApplyButton(self):
    """
    Run processing when user clicks "Apply" button.
    """
    try:
      # Compute output
      self.logic.process(self.ui.inputSelector.currentNode(), self.ui.outputSelector.currentNode(),self.ui.annotationROISelector.currentNode())
      
    except Exception as e:
      slicer.util.errorDisplay("Failed to compute results: "+str(e))
      import traceback
      traceback.print_exc()

  def onCheckedShowROI(self):
    node = self._parameterNode.GetNodeReference("ROINode")
    if self.ui.showROICheckBox.checked == True:
      print("show")
      node.SetDisplayVisibility(True)
    else:
      print("not show")
      node.SetDisplayVisibility(False)
  
  def onResetButton(self):
    transform_node = self._parameterNode.GetNodeReference("TransformNode")
    if transform_node:
      rotationMatrix = vtk.vtkMatrix4x4()
      rotationMatrix.Identity()
      transform_node.SetMatrixTransformToParent(rotationMatrix)
      self.updateGUIFromParameterNode()
'''
  def onRegister(self):
    ROINode = self._parameterNode.GetNodeReference("ROINode")
    if self._parameterNode.GetNodeReference("ROINode"):
'''
  


#
# cropLogic
#

class cropLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self):
    """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
    ScriptedLoadableModuleLogic.__init__(self)

  def setDefaultParameters(self, parameterNode):
    """
    Initialize parameter node with default settings.
    """
    if not parameterNode.GetParameter("Threshold"):
      parameterNode.SetParameter("Threshold", "100.0")
    if not parameterNode.GetParameter("Invert"):
      parameterNode.SetParameter("Invert", "false")

  def process(self, inputVolume, outputVolume, ROINode, showResult=True):
    """
    Run the processing algorithm.
    Can be used without GUI widget.
    :param inputVolume: volume to be thresholded
    :param outputVolume: thresholding result
    :param imageThreshold: values above/below this threshold will be set to 0
    :param invert: if True then values above the threshold will be set to 0, otherwise values below are set to 0
    :param showResult: show output volume in slice viewers
    """

    if not inputVolume or not outputVolume:
      raise ValueError("Input or output volume is invalid")

    import time
    startTime = time.time()
    logging.info('Processing started')

    parameter = slicer.vtkMRMLCropVolumeParametersNode()
    parameter.SetInputVolumeNodeID(inputVolume.GetID())
    parameter.SetOutputVolumeNodeID(outputVolume.GetID())
    parameter.SetROINodeID(ROINode.GetID())

    slicer.modules.cropvolume.logic().Apply(parameter)

    stopTime = time.time()
    logging.info('Processing completed in {0:.2f} seconds'.format(stopTime-startTime))

#
# cropTest
#

class cropTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear()

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_crop1()

  def test_crop1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")

    # Get/create input data

    import SampleData
    registerSampleData()
    inputVolume = SampleData.downloadSample('crop1')
    self.delayDisplay('Loaded test data set')

    inputScalarRange = inputVolume.GetImageData().GetScalarRange()
    self.assertEqual(inputScalarRange[0], 0)
    self.assertEqual(inputScalarRange[1], 695)

    outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
    threshold = 100

    # Test the module logic

    logic = cropLogic()

    # Test algorithm with non-inverted threshold
    logic.process(inputVolume, outputVolume, threshold, True)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], threshold)

    # Test algorithm with inverted threshold
    logic.process(inputVolume, outputVolume, threshold, False)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], inputScalarRange[1])

    self.delayDisplay('Test passed')
