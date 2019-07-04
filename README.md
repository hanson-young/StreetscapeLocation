# StreetscapeLocation
“交通银行杯”第六届中国研究生智慧城市技术与创意设计大赛

- [x] 纠正图像 主要代码distort.py  
[参考](https://blog.csdn.net/hpuhjl/article/details/80899931)  

- [x] 图像搜索   
[参考](https://github.com/zibuyu1995/ApplicationInImageProcessing/tree/master/orb_image_search)

- [ ] 确定大概定位（初赛阶段）   

- [ ] 双目视觉配准PCL[参考](https://www.cnblogs.com/riddick/p/8486223.html)   

- [ ] 点云匹配准确定位（复赛）[参考](https://blog.csdn.net/wishchin/article/details/74279021)  



### 1.0版操作流程：
- 数据集处理，将每个scence中的全景图thumbnail.jpg提取出来并按照子文件夹名称重新命名，组成新的数据集文件query_scenceK和gallery_scenceK:

```python
python datasets_pano.py
```

- gallery特征提取，并按照不同的scence分别存储为datasetK.db:
```python
python orb_search/generate_index.py
```

- 提取query图像特征并与gallery做匹配，输出top6匹配的gallery图像名称及匹配点数，保存为文件query_gallery_search.csv和query_gallery_value.csv:
```python
python query_gallery_search.py
```

- 根据top6（或者不全用）匹配计算query的相机坐标并保存为文件my_result.csv:
```python
python coordinate.py
```

- 注：记得更改文件路径，方法略暴力，提升空间很大，诸君加油
