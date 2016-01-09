---
layout: page
title: "PointSetProcessing"
category: doc
date: 2016-01-06 10:16:55
order: 3
---
PointSetProcessing is a module for 3D Slicer which can perform some common point-set processing tasks:

* **Downsampling**: Downsampling of an input-point set using [1].

* **Outlier removal**: Outliers removal from an input point-set using [3].

* **Estimate normals**:  Approximate normals of an input point-set, which can be done using either [2] or [3,4]. In order to perform the Poisson surface reconstruction, the normals of the point set *has* to be constructed.  For the reconstruction mehod based on Delaunay triangulation, this is *not* necessary.

* **Surface reconstruction**: The surface reconstruction implementation uses either Possion surface reconstruction [5, 6] or Delaunay triangulation [7].

<p align="center">
<img src="https://raw.githubusercontent.com/HGGM-LIM/ConoSurf/gh-pages/images/Fig3b.PNG" alt="Fig3b" align="middle" style="width: 600px;"/>
</p>
</p>
<p align="center">
<b>Figure 4.</b> The PointSetProcessing module which performs surface reconstruction from sets of unorganized points as well as other common point-set processing tasks.
</p>

#### Build Instructions
1. **3D Slicer**: Follow the instructions found [here](http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Developers/Build_Instructions)
2. **vtkInfoVisBoost**: Download the latest version of Boost from [here] (http://www.boost.org/users/history/version_1_59_0.html), and extract to a folder of your choice (BOOST_ROOT). Open CMake and set the build directory to the VTK-build folder located in your 3D Slicer build. Add an entry called BOOST_ROOT, enable vtkInfoVisBoost and vtkInfoVisBoostGraphAlgorithms, then press Generate. Open the Slicer.sln located in the top directory of your Slicer build and build Slicer again.
4. **PoissonReconstruction**: Build the PoissonReconstruction library located [here]( https://github.com/daviddoria/PoissonReconstruction), and link it with the VTK-build located in your 3D Slicer build folder.
5. **PointSetProcessing VTK library**: Build the PointSetProcessing VTK library located [here](https://github.com/daviddoria/PointSetProcessing), and link it with the VTK-build located in your 3D Slicer build folder.
6. **PointSetProcessing module**: Get the PointSetProcessing 3D Slicer module source code from [here](https://github.com/HGGM-LIM/ConoSurf/). Then build the module after adding: the PoissonReconstruction library, build folder and includes; the PointSetProcessing library and includes; and the vtkInfovisBoostGraphAlgorithms library, in CMake. Make sure as well to add the directory containing vtkPoissonReconstruction.dll to your Windows path.
7. **Add the module to 3D Slicer**: The PointSetProcessing module is a mixed loadable and scriptable module. So, to add the module to 3D Slicer, first point 3D Slicer to the folder which contains `PointSetProcessingPy.py` (via Edit -> Application Settings -> Modules -> Additional module paths -> Add). Second, point 3D Slicer to the module binaries [BUILD_DIR]\lib\Slicer-4.4\qt-loadable-modules\[Release/Debug]. Restart 3D Slicer and the module should now be available through the module selector in 3D Slicer (under the IGT category).

#### Usage
For a basic use-case scenario, add the sample point-set, obtained from a breast phantom (`Points_Breast_phantom.vtp`), available in the Data folder of the PointSetProcessing module to 3D Slicer. Start the PointSetProcessing module and under the Compute Normals widget, set Radius to 25.00 and K-Nearest Neighbors to 15. Press Apply and green arrows, representing the estimated normals will appear in the 3D view. Next, go to the Compute Surface widget and set Depth to 6.0 and Scale to 1.00. Press Apply and a red surface, reconstructed from the input point-set and its estimated normals, will appear in the 3D view.

<p align="center">
<img src="https://raw.githubusercontent.com/HGGM-LIM/ConoSurf/gh-pages/images/PP_sample.PNG" alt="PP_sample" align="middle" style="width: 600px;"/>
</p>
</p>
<p align="center">
<b>Figure 5.</b> Output from the basic use-case scenario on the `Points_Breast_phantom.vtp` data-set. Top) Results from estimating the normals. Bottom) Results from computing the surface.
</p>

#### Bibliography
1. http://www.vtk.org/doc/nightly/html/classvtkCleanPolyData.html
2. http://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html
3. http://daviddoria.com/a-point-set-processing-toolkit-for-vtk/
4. Hoppe, Hugues, et al. Surface reconstruction from unorganized points. Vol. 26. No. 2. ACM, 1992.
5. Kazhdan, Michael, Matthew Bolitho, and Hugues Hoppe. "Poisson surface reconstruction." Proceedings of the fourth Eurographics symposium on Geometry processing. Vol. 7. 2006.
6. Doria D., Gelas A. Poisson Surface Reconstruction for VTK. 2010 Mar (with minor changes/improvements by me)
7. http://www.vtk.org/doc/nightly/html/classvtkDelaunay3D.html 


