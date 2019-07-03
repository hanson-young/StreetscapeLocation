# StreetscapeLocation
“交通银行杯”第六届中国研究生智慧城市技术与创意设计大赛

- [x] 纠正图像 主要代码distort.py  
[参考](https://blog.csdn.net/hpuhjl/article/details/80899931)  

- [ ] 图像搜索   
[参考](https://github.com/zibuyu1995/ApplicationInImageProcessing/tree/master/orb_image_search)

- [ ] 确定大概定位（初赛阶段）   

- [ ] 双目视觉配准PCL[参考](https://www.cnblogs.com/riddick/p/8486223.html)   

- [ ] 点云匹配准确定位（复赛）[参考](https://blog.csdn.net/wishchin/article/details/74279021)  



### 图像搜索大致流程：
- 建立一个tiny database，命名dataset.db，存有所有gallery image的feature，后续可将每个gallery image对应的location一并存入database，
方便检索与结果写入；

```python
python generate_index.py
```

- 对于每个query image，对其提取特征后，与gallery database对比，对比方式为暴力枚举或KNN，输出格式为：(图片名称，匹配特征点个数)；
```python
python img_search.py
```

- 注：gallery_img文件夹中图片包含了query_img中所有图片，主要是想测试以下算法能不能不能够检索出“自己”；图像搜索效果不是很理想。
