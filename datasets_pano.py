import os
import os.path as osp
import cv2
import numpy as np
import glob
root = '/data1/lml/smart_city/scene1_jiading_lib_test/'
save_dir = '/home/lml/smart_city/StreetscapeLocation/query_sence1/'
root0 = root + '/*'
if not osp.isdir(save_dir):
    os.makedirs(save_dir)
for sence in glob.glob(root0):
    #print(sence)
    name_tuple = osp.split(sence)
    name = name_tuple[1] + '.png'
    #print(name)
    root_path = sence + '/thumbnail.jpg'
    #print(root_path)
    gallery_img = cv2.imread(root_path)
    img_path = save_dir + name
    print(img_path)
    cv2.imwrite(img_path, gallery_img)
