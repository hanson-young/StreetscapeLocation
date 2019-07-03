from tinydb import TinyDB
from operator import itemgetter

from orb_search.orb_feature_matches import generate_image_feature
from orb_search.orb_feature_matches import knn_match, bf_match


from config import (
    match_type, query_img,
    cpu_count, knn_match_num, bf_match_num
)

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


if __name__ == '__main__':
    
    db = TinyDB('../dataset.db')
    table = db.table('feature')
    cache_features = table.all()[0]
    
    img_path = query_img
    
    match_result = image_search(img_path)
    print(match_result)