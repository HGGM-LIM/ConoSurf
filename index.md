---
layout: default
title: "Jekyll Docs Template"
---

## ConoSurf:
#### Open-source 3D scanning system based on a conoscopic holography device for acquiring surgical surfaces
---
#### Introduction
A major diffculty in image guided therapy (IGT) is acquiring the patient's anatomy intraoperatively, which can be used for registering preoperative information. Intraoperative use of standard modalities has several limitations, such as low image quality (ultrasound), radiation exposure (computed tomography) or high costs (magnetic resonance imaging). An alternative approach is using a tracked pointer and registering the acquired points to surfaces identified in preoperative images. However, the pointer may cause tissue deformations and may additionally have difficulty in accessing narrow cavities during an intraoperative procedure. Recent proposals, utilizing a tracked conoscopic holography device, have shown promising results without the previously mentioned drawbacks.

Therefore, we present an open-source software system -- based on [3D Slicer](https://www.slicer.org/) and the [Plus Toolkit](https://www.assembla.com/spaces/plus/wiki) -- which enables real-time surface scanning using a conoscopic holography device and a wide variety of tracking systems. Our system is integrated into preexisting and well supported software solutions. We have evaluated the system's target registration error (TRE) with respect to point measurements and its surface registration error (SRE) when reconstructing a surface mesh from the acquired points. The system could acquire and visualize points at a rate of 50 Hz. The mean TRE of point measurements was 1.46 mm. For a quick guidance scan (an IGT scenario), where a low number of points were obtained, surface reconstruction improved the SRE compared to point-set registration.