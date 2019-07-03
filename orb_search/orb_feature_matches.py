# coding: utf-8

import cv2
import numpy as np
from config import maximum_features, scale_factor


def generate_image_feature(image_path: str, is_dumps: bool) -> tuple:
    """
    生成图像特征点
    :param is_dumps: 是否压缩
    :param image_path: 图像路径
    """
    image_uid = image_path[image_path.rfind("/") + 1:][:6]
    images = cv2.imread(image_path)
    orb = cv2.ORB_create(maximum_features, scale_factor)
    (kp, des) = orb.detectAndCompute(images, None)
    if is_dumps:
        feature = des.tolist()
    else:
        feature = des
    return image_uid, feature

def knn_match(search_feature, feature):
    """ knn """
    feature = np.array(feature, dtype='uint8')
    bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf_matcher.knnMatch(search_feature, trainDescriptors=feature, k=2)
    good_matches = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
    return len(good_matches)


def bf_match(search_feature, feature):
    """ 蛮力匹配(保留最大的特征点数目) """
    feature = np.array(feature, dtype='uint8')
    bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf_matcher.match(search_feature, feature)
    return len(matches)