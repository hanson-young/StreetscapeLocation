import yaml
import numpy as np

import cv2

fs = cv2.FileStorage("calibration.yaml", cv2.FILE_STORAGE_READ)
fn = fs.getNode("distort_camera6")
print(fn.mat())