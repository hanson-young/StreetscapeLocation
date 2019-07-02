import cv2
import numpy as np

img_found = 'origin_1.jpg'
img = cv2.imread(img_found)
img = cv2.resize(img,(640,480))
_img_shape = img.shape[:2]
DIM = _img_shape[::-1]
camera_matrix = np.array([[ 1.9469000000000000e+02, 0., 3.2046899999999999e+02],
                          [0., 1.9399400000000000e+02, 2.3898800000000000e+02],
                          [0., 0., 1. ]])

dist_coefs = np.array([[ -2.6072300000000000e-02, 4.8158400000000001e-03,
       -4.9776700000000000e-03, 1.0583000000000001e-03]])
map1, map2 = cv2.fisheye.initUndistortRectifyMap(camera_matrix, dist_coefs, np.eye(3), camera_matrix, DIM,cv2.CV_16SC2)
undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)

# crop and save the image
outfile = img_found + '_undistorted.png'
print('Undistorted image written to: %s' % outfile)
cv2.imshow(outfile, undistorted_img)
cv2.waitKey(0)