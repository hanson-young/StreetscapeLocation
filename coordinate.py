#coding=utf-8
import os
import os.path as osp
import cv2
import csv
import matplotlib.pyplot as plt
import glob


query_gallery_search = 'query_gallery_search.csv'
query_gallery_value = 'query_gallery_value.csv'
sence_csv = '/home/lml/smart_city/StreetscapeLocation/sence_csv/*.csv'
example_result = 'example_result.csv'
my_result = 'my_result_3.csv'
search_datas = []
sence_list = []
gallery_values = []

for csv_path in glob.glob(sence_csv):
    csv_file = osp.split(csv_path)
    csv_name = osp.join('sence_csv/', csv_file[1])
    with open(csv_name) as f:
        f_csv = csv.reader(f)
        f_header = next(f_csv)
        for row in f_csv:
            sence_list.append(row)
print(len(sence_list))


with open(query_gallery_search) as f:
    f_csv = csv.reader(f)
    f_header = next(f_csv)
    for row in f_csv:
        search_datas.append(row)
with open(query_gallery_value) as f:
    f_csv = csv.reader(f)
    f_header = next(f_csv)
    for row in f_csv:
        gallery_values.append(row)

# change list coordinate_values to dict
sence_dict = {}
'''
x_min = 900
x_max = 0
y_min = 900
y_max = 0
'''

for i, item in enumerate(sence_list):
    coordinate = [float(item[1]), float(item[2]), float(item[3])]
    '''
    if coordinate[0] > x_max: x_max = coordinate[0]
    if coordinate[0] < x_min: x_min = coordinate[0]
    if coordinate[1] > y_max: y_max = coordinate[1]
    if coordinate[1] < y_min: y_min = coordinate[1]
    '''

    sence_dict[item[0]] = coordinate

query_co = []
query_coordinates = []
#search_datas = search_datas[0:10]
coordinate_values = []
for i, search_data in enumerate(search_datas):
    x = []
    y = []
    z = []
    coordinates = []
    values = [0, 0, 0, 0, 0, 0, 0]
    for j in range(1, 3):
        values[j] = int(gallery_values[i][j])
        coordinate = sence_dict[search_data[j]]
        x.append(coordinate[0])
        y.append(coordinate[1])
        z.append(coordinate[2])
        coordinates.append(coordinate)
    values.remove(0)
    x_list = [a * b for a, b in zip(values, x)]
    y_list = [a * b for a, b in zip(values, y)]
    z_co = sum(z)/len(z)
    x_co = sum(x_list)/sum(values)
    y_co = sum(y_list)/sum(values)
    #plt.xlim(x_min, x_max)
    #plt.ylim(y_min, y_max)
    #plt.scatter(x, y, marker='*', color='red')
    #plt.scatter(x_co, y_co, marker='X', color='green')
    #plt.show()
    query_co = [search_data[0], x_co, y_co, z_co]
    query_coordinates.append(query_co)

results = []
with open(example_result) as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        results.append(row)

for i, item in enumerate(results):
    for j, query_co in enumerate(query_coordinates):
        if item[0] == query_co[0]:
            item[1:4] = query_co[1:4]

with open(my_result, 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerows(results)





