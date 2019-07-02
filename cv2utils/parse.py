import yaml
import numpy as np

import cv2
fs = cv2.FileStorage("calibration.yaml", cv2.FILE_STORAGE_READ)
fn = fs.getNode("intri_camera1")
print(fn.mat())