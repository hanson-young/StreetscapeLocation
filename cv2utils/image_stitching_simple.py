# import the necessary packages
from imutils import paths
import os
import os.path as osp
import numpy as np
import argparse
import imutils
import cv2
import glob


def rotate(image, angle):
    (h, w) = image.shape[:2]
    (cx, cy) = (w//2, h//2)
    M = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nw = int((h * sin) + (w * cos))
    nh = int((h * cos) + (w * sin))
    M[0, 2] += (nw/2) - cx
    M[1, 2] += (nh/2) - cy
    rotated = cv2.warpAffine(image, M, (nw, nh))
    return rotated

images = []
root = '/data1/lml/calibration/scene1_jiading_lib_test/PIC_20190522_100509/*'
save_path = 'images/'
output = 'images/output.png'
if not osp.isdir(save_path):
    os.makedirs(save_path)
for img_path in glob.glob(root):
    image = cv2.imread(img_path)
    img90 = rotate(image, 90)
    img_name = osp.split(img_path)
    name = img_name[1]
    save_name = save_path + name
    cv2.imwrite(save_name, img90)
    images.append(img90)

# initialize OpenCV's image stitcher object and then perform the image stitching
print("[INFO] stitching images...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

# if the status is '0', then OpenCV successfully performed image stitching
if status == 0:
    # write the output stitched image to disk
    cv2.imwrite(output, stitched)
    # display the output stitched image to our screen
    cv2.imshow("Stitched", stitched)
    cv2.waitKey(0)
    # otherwise the stitching failed, likely due to not enough keypoints) being detected
else:
    print("[INFO] image stitching failed ({})".format(status))

