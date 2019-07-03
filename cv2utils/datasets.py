#-*- coding:utf-8 -*-
import os
import os.path as osp
import cv2
import numpy as np
import glob


def calibration(img, n):
    intri = "intri_camera" + n
    distort = "distort_camera" + n
    f_intri = fs.getNode(intri)
    f_distort = fs.getNode(distort)
    camera_matrix = f_intri.mat()
    dist_coefs = f_distort.mat()
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(camera_matrix, dist_coefs, np.eye(3), camera_matrix, DIM,
                                                     cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img


fs = cv2.FileStorage("calibration.yaml", cv2.FILE_STORAGE_READ)
root = '/data1/lml/smart_city/'
save_dir = '/data1/lml/calibration/'
root0 = root + '/*'
for sence in glob.glob(root0):
    sence_dir = osp.split(sence)
    data_dir = sence_dir[1] + '/*'
    data_dir = osp.join(root, data_dir)
    for dir_name in glob.glob(data_dir):
        l = len(root)
        save_path = osp.join(save_dir, dir_name[l:])
        img_paths = glob.glob(osp.join(dir_name, '*.jpg'))
        for fname in img_paths:
            if fname[-13:] == 'thumbnail.jpg' or fname[-8:] == 'pano.jpg':
                continue
            else:
                img = cv2.imread(fname)
                img = cv2.resize(img, (640, 480), cv2.INTER_LINEAR)
                _img_shape = img.shape[:2]
                DIM = _img_shape[::-1]
                n = fname[-5]
                undistorted_img = calibration(img, n)
                # crop and save the image
                if not osp.isdir(save_path):
                    os.makedirs(save_path)
                outfile = save_path + '/' + fname[-12:-4] + '.png'
                print(n, outfile)
                cv2.imwrite(outfile, undistorted_img)

