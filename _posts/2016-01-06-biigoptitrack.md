---
layout: page
title: "BiiGOptitrack"
category: doc
date: 2016-01-06 10:17:02
order: 4
---
The BiiGOptitrack library is a hardware interface which communicates with the multi-camera optical tracking system OptiTrack provided by the company [NaturalPoint Inc](http://www.optitrack.com/). OptiTrack already provides an application programming interface (API) in order to control the multi-camera optical tracking system. However, controlling the tracker hardware directly using the API is not suitable for clinical applications where error handling is mandatory for proper system error recovery. Hence, we have developed the BiiGOptitrack library to interface with the tracker. BiiGOptitrack follows the tracking interface standard defined by the OpenIGTLink protocol, allowing for connection to the tracker, tracked tools management and safe recovery from errors during tracking acquisition. The most interesting advantage of BiiGOptitrack is the threading-based tracking that allows for real-time data acquisition whilst ensuring tracked tools are inside the field of view of the cameras, all markers forming the rigid-bodies are visible and time-stamps correspond to the delivered data through the library interface. Such information plays a critical role during further time and spatial calibrations. 

#### API Documentation
API documentation, generated through Doxygen, can be found [here](
http://hggm-lim.github.io/BiiGOptitrack) (currently work in progress).

#### Build Instructions
Details on how to build BiiGOptitrack will be published here shortly.

#### Plus integration
The OptiTrack tracking system is currently not supported by the Plus Toolkit, but we are working on adding this support through the BiiGOptitrack library (see the corresponding Plus Assembla [ticket](https://www.assembla.com/spaces/plus/tickets/1018-add-support-for-optitrack-tracking-systems-/details)). Until then, we will provide our own Plus build (PlusLIM) where BiiGOptitrack is fully integrated, and therefore supports the OptiTrack. The source code for this Plus version can be downloaded from [here](https://github.com/HGGM-LIM/PlusLIM). The build procedure is equal to the one described in the ConoProbeConnector section (under Plus Integration) and OptiTrack support is enabled by checking PLUS_USE_OPTITRACK in CMake.
