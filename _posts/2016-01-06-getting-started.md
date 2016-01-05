---
layout: page
title: "Getting Started"
category: doc
date: 2016-01-06 10:16:36
order: 1
---
The ConoSurf project consists of three seperate, stand-alone tools:

* **ConoProbeConnector**: A module for 3D Slicer which can aquire and visualize point-sets from a tracked ConoProbe single-point measurement device. Hardware interfacing is implemented through the Plus Toolkit.
* **PointSetProcessing**: A module for 3D Slicer which performs common point-set processing tasks. A point-set could, for example, have been obtained using the ConoProbeConnector module.
* **BiiGOptitrack**: A C++ library which interfaces with an OptiTrack multi-camera tracking system.

By stand-alone, we mean that they can be built and used on their own, for their respective purpose. Additionally, they can also be used in combination, in particular to create 3D models of real-world objects. In particular, the results we mention on the introduction page, were obtained using a combination of all three: the BiiGOptitrack-library, to interface with a multi-camera optical tracking system and the Plus Toolkit; the ConoProbeConnector module, to connect to the data streams, and to visualize and save the recorded points; and the PointSetProcessing module, to reconstruct 3D surfaces from the obtained point-set.

For more details on each separate tool (like build instructions and use-case examples), see its corresponding section in the sidebar (*ConoProbeConnector*, *PointSetProcessing*, *BiiGOptitrack*). Note that the build instructions for each tool are closely related since they are based on simillar toolkits and libraries.

<p align="center">
<img src="https://raw.githubusercontent.com/HGGM-LIM/ConoSurf/gh-pages/images/Fig1.PNG" alt="Fig1" align="middle" style="width: 600px;"/>
</p>
<p align="center">
<b>Figure 2.</b> The implementation overview of the 3D scanning system. The data from the ConoProbe and the Optitrack is obtained through the Plus Toolkit and the BiiGOptitrack library. This data is then transmitted, via OpenIGTLink, to 3D Slicer where the modules are made available.
</p>