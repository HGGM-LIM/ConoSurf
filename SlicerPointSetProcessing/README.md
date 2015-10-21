# SlicerPointSetProcessing
SlicerPointSetProcessing is a module for 3D Slicer which can perform common point-set processing tasks such as outlier removal, normals estimation and surface reconstruction, using various methods.

### Downsampling
Downsampling of the input point set is performed using [1].

### Outlier removal
Outliers removal from the input point set is performed using [3].

### Estimate Normals
In order to perform the Poisson surface reconstruction, the normals of the point set has to be approximated. This can be done using either [2] or [3,4]. For the reconstruction mehod based on Delaunay triangulation, this is not necessary.

### Surface Reconstruction
The surface reconstruction uses either Possion surface reconstruction [5, 6] or Delaunay triangulation [7].

## Build Instructions
1. **3D Slicer** - Follow the instructions found here: http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Developers/Build_Instructions
2. **vtkInfoVisBoost** - Download the latest version of Boost from here: http://www.boost.org/users/history/version_1_59_0.html, and extract to a folder of your choice (BOOST_ROOT). Open CMake and set the build directory to the VTK-build folder located in your 3D Slicer build. Add an entry called BOOST_ROOT, enable vtkInfoVisBoost and vtkInfoVisBoostGraphAlgorithms, then press Generate. Open the Slicer.sln located in the top directory of your Slicer build and build Slicer again.
4. **PoissonReconstruction** - Build the PoissonReconstruction library located here: https://github.com/daviddoria/PoissonReconstruction, and link it with the VTK-build located in your 3D Slicer build folder.
5. **PointSetProcessing** - Build the PointSetProcessing library located here: https://github.com/daviddoria/PointSetProcessing, and link it with the VTK-build located in your 3D Slicer build folder.
6. **SlicerPointSetProcessing** - Build the SlicerPointSetProcessing module after adding: the PoissonReconstruction library, build folder and includes; the PointSetProcessing library and includes; and the vtkInfovisBoostGraphAlgorithms library, in CMake. Make sure as well to add the directory containing vtkPoissonReconstruction.dll to your Windows path.

## TODO
* Add smoothing
* Show/hide input points
* Set glyph size
* If there is interest: Reset to default, save params in Slicer.ini, calculate in separate thread

## Bibliography
1. http://www.vtk.org/doc/nightly/html/classvtkCleanPolyData.html
2. http://www.vtk.org/doc/nightly/html/classvtkPolyDataNormals.html
3. http://daviddoria.com/a-point-set-processing-toolkit-for-vtk/
4. Hoppe, Hugues, et al. Surface reconstruction from unorganized points. Vol. 26. No. 2. ACM, 1992.
5. Kazhdan, Michael, Matthew Bolitho, and Hugues Hoppe. "Poisson surface reconstruction." Proceedings of the fourth Eurographics symposium on Geometry processing. Vol. 7. 2006.
6. Doria D., Gelas A. Poisson Surface Reconstruction for VTK. 2010 Mar (with minor changes/improvements by me)
7. http://www.vtk.org/doc/nightly/html/classvtkDelaunay3D.html 
