# coding=utf-8
'''
This script is utilized to generate index/database of panoramas in various scenes so as to facilitate feature search.
'''
import cv2
import glob
import asyncio
import uvloop
from tinydb import TinyDB
from concurrent.futures import ProcessPoolExecutor


from config import gallery_path, cpu_count
from config import maximum_features, scale_factor

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def generate_image_feature(image_path: str, is_dumps: bool) -> tuple:
    """
    generate image feature
    :param is_dumps: compress or not?
    :param image_path: image path
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


def feature_persistence(task_results: list) -> int:
    '''
    :param task_results: feature
    :return:
    '''
    feature_dict = dict(task_result.result() for task_result in task_results)

    db = TinyDB('../dataset.db')
    table = db.table('feature')
    table.insert(feature_dict)
    feature_count = len(feature_dict)
    return feature_count
    
    
async def generate_image_index(eve_loop, processes_executor):
    """ 多进程生成图像索引 """
    image_feature_tasks = []
    task_append = image_feature_tasks.append
    for image_path in glob.glob(gallery_path + "/*.png"):
        task_append(
            eve_loop.run_in_executor(
                processes_executor, generate_image_feature, image_path, True
            )
        )
    task_results, _ = await asyncio.wait(image_feature_tasks)
    feature_count = feature_persistence(task_results)
    print(f"{feature_count}幅图像完成索引")
    

if __name__ == '__main__':
    executor = ProcessPoolExecutor(max_workers=cpu_count)
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            generate_image_index(event_loop, executor)
        )
    finally:
        event_loop.close()