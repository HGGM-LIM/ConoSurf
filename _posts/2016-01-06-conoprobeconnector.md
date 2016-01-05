---
layout: page
title: "ConoProbeConnector"
category: doc
date: 2016-01-06 10:16:46
order: 2
---
ConoProbeConnector is a module for 3D Slicer which can aquire and visualize point-sets from a tracked conoscopic holography single-point measurement device called a [ConoProbe](http://www.optimet.com/3dmeasurementsystem-products.php), where the measurement and tracking data is sent using the 3D Slicer supported [OpenIGTLink protocol](http://openigtlink.org/). As part of the ConoProbeConnector project we also made the ConoProbe device fully supported by the Plus Toolkit. This support means that the ConoProbe can be used with any of the tracking systems supported by Plus -- [a large number of systems](http://perk-software.cs.queensu.ca/plus/doc/nightly/user/Devices.html). The major features of the ConoProbeConnector module are:

* **Real-time, intuitive 3D visualization**: Points can be recorded and visualized in real time. By setting a principal direction and an interval, the points are coloured in order to make the acquired point-set easier to interpret. 
  
* **Live filtering and post-processing**: By setting a threshold for the signal-to-noise ratio and an interval for the distance (data from the ConoProbe), points can be filtered during acquisition.  Once data has been acquired it can also be post-processed with respect to the same parameters.
  
* **First-person view**: A reference 3D model of the ConoProbe, acquired using an Artec Eva surface scanner (Artec, CA, USA), can be loaded into the module enabling an intuitive first-person view during acquisition.
  
* **Recording and simulating**: The recorded point-set can be saved both in CSV and VTK format (the CSV-file includes also measurement and tracking information). Additionally, the entire Plus data stream can be recorded and replayed.

<p align="center">
<img src="https://raw.githubusercontent.com/HGGM-LIM/ConoSurf/gh-pages/images/Fig3a.PNG" alt="Fig3a" align="middle" style="width: 600px;"/>
</p>
<p align="center">
<b>Figure 1.</b> The ConoProbeConnector module which interfaces with a ConoProbe and a tracking system (with a photo of an acquisition process superimposed).
</p>

#### Build Instructions
1. **3D Slicer**: Detailed instructions on how to build 3D Slicer can be found [here](http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Developers/Build_Instructions).
2. **SlicerIGT**: The ConoProbeConnector module uses some features available through the SlicerIGT extension. In particular the Viewpoint module, which is currently *not* avaialbe though the 3D Slicer Extension Manager version of SlicerIGT. Therefore, follow the instructions found [here](https://github.com/SlicerIGT/SlicerIGT/wiki/Developers-guide) to add SlicerIGT, and make sure to check SLICERIGT_ENABLE_EXPERIMENTAL_MODULES in CMake.
3. **ConoProbeConnector**: The ConoProbeConnector module is a scriptable module, meaning that no build is required. So, to add the module to 3D Slicer, just get the source code from [here](https://github.com/HGGM-LIM/ConoSurf/) and point 3D Slicer to the folder which contains `ConoProbeConnector.py` (via Edit -> Application Settings -> Modules -> Additional module paths -> Add). The module should now be available through the module selector in 3D Slicer (under the IGT category).

#### Usage
As written at the top of this page, the ConoProbeConnector can be used with a large number of tracking systems if combined with Plus. Therefore, we recommend to build Plus (with ConoProbe support):

1. **The Plus Toolkit**: Detailed instructions on how to build the Plus Toolkit can be found [here](https://www.assembla.com/spaces/plus/wiki/Developers_guide). 
2. **ConoProbe support**: In order to have support for the ConoProbe device it is necessary to enable PLUS_USE_OPTIMET_CONOPROBE in the CMake configuration of Plus and then point CMake to the required ConoProbe Smart32 binaries obtained from [here](http://www.optimet.com/smart32-sdk.php). For more information on Plus and the ConoProbe see the corresponding info in Plus' users manual (found [here](http://perk-software.cs.queensu.ca/plus/doc/nightly/user/DeviceOptimetConoProbe.html)).

Once this is done, the PlusServer app will be available in the Plus binary folder. PlusServer can then be used to connect to the ConoProbe, and a tracking system of choice, given a Plus config-file. For a sample config file, combining the ConoProbe with an NDI Aurora optical tracker, see the Data folder of the ConoProbeConnector folder. Note that both a spatial and a temporal calibration is necessary in order to find the temporal and spatial offset between the tracker and the ConoProbe. These procedures are detailed in our paper "Open-source 3D scanning system based on a conoscopic holography device for acquiring surgical surfaces" which, hopefully, soon will be published and then referenced here.