import numpy as np
import cv2
import os
import os.path as osp
import csv
import glob
from tinydb import TinyDB
from operator import itemgetter
from orb_search.orb_feature_matches import generate_image_feature
from orb_search.orb_feature_matches import knn_match, bf_match

from multiprocessing import cpu_count


cpu_count = cpu_count()
maximum_features = 618  # orb算法获取图像最大特征点
scale_factor = 1.5  # 缩放因子
match_type = 1  # 1 knn, 2 bf 匹配方式
knn_match_num = 1  # knn 最少匹配数(需要依据maximum_features来动态调整)
bf_match_num = 256  # bf 方式最少匹配数(需要依据maximum_features来动态调整)


def image_search(image_path=None):
    """ image searching """
    global cache_features

    match_results = []
    match_results_append = match_results.append
    search_feature = generate_image_feature(image_path, False)[1]
    for image_uid, feature in cache_features.items():
        if match_type == 1:
            # knn 匹配
            match_num = knn_match(search_feature, feature)
            if match_num < knn_match_num:
                # 少于knn_match_num个特征点就跳过
                continue
        else:
            match_num = bf_match(search_feature, feature)
            # 蛮力匹配
            if match_num < bf_match_num:
                # 少于bf_match个特征点就跳过
                continue
        match_results_append((image_uid, match_num))
    match_results = sorted(match_results, key=itemgetter(1), reverse=True)
    return match_results


root = '/home/lml/smart_city/StreetscapeLocation/'
query = osp.join(root, 'query/query_sencex/*.png')
db_path = '/home/lml/smart_city/StreetscapeLocation/datasets_db/datasetx.db'
search_list = []
value_list = []
for n in range(1, 9):
    s = list(query)
    s[query.rfind("/") - 1] = str(n)
    query = ''.join(s)
    s = list(db_path)
    s[-4] = str(n)
    db_path = ''.join(s)
    print(db_path)
    for img_path in glob.glob(query):
        db = TinyDB(db_path)
        table = db.table('feature')
        cache_features = table.all()[0]
        match_result = image_search(img_path)
        print(match_result)

        query_name = img_path[img_path.rfind("/") + 1: img_path.rfind(".")]
        row1 = [query_name, match_result[0][0], match_result[1][0], match_result[2][0], match_result[3][0],
                match_result[4][0], match_result[5][0]]
        row2 = [query_name, match_result[0][1], match_result[1][1], match_result[2][1], match_result[3][1],
                match_result[4][1], match_result[5][1]]
        search_list.append(row1)
        value_list.append(row2)
        print(row1)
        print(row2)

    path1 = 'query_gallery_search.csv'
    path2 = 'query_gallery_value.csv'
    csv1_head = ['query', 'gallery1', 'gallery2', 'gallery3', 'gallery4', 'gallery5', 'gallery6']
    csv2_head = ['query', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6']

    with open(path1, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(csv1_head)
        f_csv.writerows(search_list)

    with open(path2, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(csv2_head)
        f_csv.writerows(value_list)

