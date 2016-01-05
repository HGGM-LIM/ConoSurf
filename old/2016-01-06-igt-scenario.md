---
layout: page
title: "IGT Scenario"
category: doc
date: 2016-01-06 16:37:55
order: 5
---
In this section we will describe a simple IGT scenario which makes use of the three tools previously described. The IGT scenario in question details acquring surface points from a breast phantom using the ConoProbe (tracked by an OptiTrack optical tracker). The acquired surface points are then reconstructed into a surface and a CT scan of the same breast phantom is registered to the scene. 3D Slicer, SlicerIGT and the Plus Toolkit are all cornerstone pieces in this process. Important to point out is that we choose to utilize an OptiTrack tracker
 
The prerequisites of this section are that 3D Slicer, SlicerIGT, PlusLIM (with the options PLUS_USE_OPTITRACK and PLUS_USE_OPTIMET_CONOPROBE enabled), PointSetProcessing and ConoProbeConnector -- as detailed in the previous sections -- are built/installed. Additionally, a temporal and a spatial calibration needs to have been performed between the ConoProbe and the OptiTrack.
