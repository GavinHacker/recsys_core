# 推荐系统

    基于机器学习方法的电影推荐系统
    v0.10
    
### 💡QQ讨论群： 641914109

## 整体介绍

* recsys_ui: 前端技术(html5+JavaScript+jquery+ajax)
* recsys_web: 后端技术(Java+SpringBoot+mysql)
* recsys_spider: 网络爬虫(python+BeautifulSoup)
* recsys_sql: 使用SQL数据处理
* recsys_model: pandas, libFM, sklearn.  pandas数据分析和数据清洗，使用libFM,sklearn对模型初步搭建
* recsys_core: 使用pandas, libFM, sklearn完整的数据处理和模型构建、训练、预测、更新的程序
* recsys_etl：ETL  处理爬虫增量数据时使用kettle ETL便捷处理数据

为了能够输出一个可感受的系统，我们采购了阿里云服务器作为数据库服务器和应用服务器，在线上搭建了电影推荐系统的第一版，地址是:

# www.technologyx.cn

可以注册，也可以使用已有用户：


用户名 | 密码
---|---
gavin | 123
gavin2 | 123
wuenda | 123

欢迎登录使用感受一下。

![image](http://upload-images.jianshu.io/upload_images/2230072-7cdaee7ab618eda5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 设计思路

![image](https://images.gitee.com/uploads/images/2019/0109/204217_b71ea240_1234921.png)

#### 用简单地方式表述一下设计思路，

##### 1.后端服务recsys_web依赖于系统数据库的推荐表‘recmovie’展示给用户推荐内容
##### 2.用户对电影打分后（暂时没有对点击动作进行响应），后台应用会向mqlog表插入一条数据（消息）。
##### 3.新用户注册，系统会插入mqlog中一条新用户注册消息
##### 4.新电影添加，系统会插入mqlog中一条新电影添加消息
##### 5.推荐模块recsys_core会拉取用户的打分消息，并且并行的做以下操作：

    a.增量的更新训练样本
    b.快速（因服务器比较卡，目前设定了延时）对用户行为进行基于内容推荐的召回
    c.训练样本更新模型
    d.使用FM，LR模型对Item based所召回的数据进行精排
    e.处理新用户注册消息，监听到用户注册消息后，对该用户的属性初始化(统计值)。
    f.处理新电影添加消息，更新基于内容相似度而生成的相似度矩阵
    

注：

* 由于线上资源匮乏，也不想使系统增加复杂度，所以没有直接使用MQ组件，而是以数据库表作为代替。
* recsys_model属于用notebook进行数据分析和数据处理以及建模的草稿，地址为：https://github.com/GavinHacker/recsys_model
* 其余的所有项目的地址索引为：https://github.com/GavinHacker/technologyx


## 模型相关的模块介绍



##### 增量的处理用户comment，即增量处理评分模块

这个模块负责监听来自mqlog的消息，如果消息类型是用户的新的comment,则对消息进行拉取，并相应的把新的comment合并到总的训练样本集合，并保存到一个临时目录
然后更新数据库的config表，把最新的样本集合(csv格式)的路径更新上去

 运行截图

![image](http://upload-images.jianshu.io/upload_images/2230072-db260d1cc802553d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

消息队列的截图

![image](http://www.vmfor.com/img/recsys/mqlog.png)


##### 把csv处理为libsvm数据

这个模块负责把最新的csv文件，异步的处理成libSVM格式的数据，以供libFM和LR模型使用，根据系统的性能确定任务的间隔时间

运行截图

![image](http://www.vmfor.com/img/recsys/把CSV数据处理为libsvm数据.png)


##### 基于内容相似度推荐

当监听到用户有新的comment时，该模块将进行基于内容相似度的推荐，并按照电影评分推荐

运行截图

![image](https://images.gitee.com/uploads/images/2019/0109/204220_57620ba7_1234921.png)


##### libFM预测

http://www.libfm.org/

对已有的基于内容推荐召回的电影进行模型预测打分，呈现时按照打分排序

如下图为打分更新

![image](http://www.vmfor.com/img/recsys/libFM预测.png)

##### 逻辑回归预测

对样本集中的打分做0，1处理，根据正负样本平衡，> 3分为喜欢 即1， <=3 为0 即不喜欢，这样使用逻辑回归做是否喜欢的点击概率预估，根据概率排序

![image](https://images.gitee.com/uploads/images/2019/0109/204230_64db3104_1234921.png)



