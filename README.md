# ARUCO Marker Detection & Camera Calibration — Short README

## 📌 Project Overview

This project performs **camera calibration** using a chessboard and **Aruco marker detection** using OpenCV.

## 📁 Project Structure

```
ARUCO/
├── camera_calibration/      # capture + calibration scripts
├── calib_data/              # MultiMatrix.npz (output)
├── generate_markers/        # ArUco generator
├── marker_detection.py      # main detection script
└── distance_check.py        # distance estimation
```

## 🔧 Camera Calibration (Short)

1. Print a **9×6 inner-corner** chessboard.
2. Run `capture_images.py` → saves many chessboard images.
3. Run `calibration_script.py` → creates **MultiMatrix.npz** containing:

   * Camera Matrix
   * Distortion Coefficients

These are later used for accurate ArUco detection.

## 🎯 ArUco Marker Detection (Short)

`marker_detection.py` uses calibration to:

* Detect ArUco markers
* Draw boxes & IDs
* Estimate distance / pose

