import cv2 as cv
import os
import numpy as np

# --- Chessboard Settings ---
CHESS_BOARD_DIM = (9, 6)        # inner corners
SQUARE_SIZE = 22                # mm (your printed square size)

# --- Termination criteria for cornerSubPix ---
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# --- Calibration data save directory ---
calib_data_path = "../calib_data"
if not os.path.isdir(calib_data_path):
    os.makedirs(calib_data_path)
    print(f'"{calib_data_path}" Directory is created')
else:
    print(f'"{calib_data_path}" Directory already Exists.')

# --- Prepare object points in real world 3D coordinates ---
# Example: (0,0,0) (1,0,0) (2,0,0) ... (8,5,0)
obj_3D = np.zeros((CHESS_BOARD_DIM[0] * CHESS_BOARD_DIM[1], 3), np.float32)
obj_3D[:, :2] = np.mgrid[0:CHESS_BOARD_DIM[0], 0:CHESS_BOARD_DIM[1]].T.reshape(-1, 2)
obj_3D *= SQUARE_SIZE   # scale by real square size

print("3D Object Points (first few):")
print(obj_3D[:10])

# --- Arrays to store points ---
obj_points_3D = []
img_points_2D = []

# --- Load captured images folder ---
image_dir_path = "images"
files = os.listdir(image_dir_path)

print("\nReading images...\n")

for file in files:
    if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
        print(f"Skipped non-image file: {file}")
        continue

    print(f"Processing: {file}")
    imagePath = os.path.join(image_dir_path, file)

    image = cv.imread(imagePath)
    if image is None:
        print(f"Could not read image: {file}")
        continue

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(gray, CHESS_BOARD_DIM, None)

    if ret:
        obj_points_3D.append(obj_3D)

        corners2 = cv.cornerSubPix(gray, corners, (3, 3), (-1, -1), criteria)
        img_points_2D.append(corners2)

        cv.drawChessboardCorners(image, CHESS_BOARD_DIM, corners2, ret)
    else:
        print(f"Chessboard NOT detected in: {file}")

cv.destroyAllWindows()

# --- Check if enough images were detected ---
if len(obj_points_3D) < 5:
    print("\n❌ Not enough valid calibration images detected!")
    print("Take at least 10–20 images from different angles.")
    exit()

# --- Calibrate the camera ---
print("\nCalibrating camera...")

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
    obj_points_3D, img_points_2D, gray.shape[::-1], None, None
)

print("Calibration Successful!")
print("\nCamera Matrix:\n", mtx)
print("\nDistortion Coefficients:\n", dist)

# --- Save calibration ---
np.savez(
    f"{calib_data_path}/MultiMatrix",
    camMatrix=mtx,
    distCoef=dist,
    rVector=rvecs,
    tVector=tvecs,
)

print("\nCalibration data saved to MultiMatrix.npz")
print("-------------------------------------------")

# --- Load to verify ---
data = np.load(f"{calib_data_path}/MultiMatrix.npz")

print("\nLoaded data:")
print("Camera Matrix:\n", data["camMatrix"])
print("Dist Coeff:\n", data["distCoef"])
