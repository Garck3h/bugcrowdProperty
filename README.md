# bugcrowdProperty
通过该工具可以实现爬取bugcrowd中有赏金的测试项目，以及项目中的资产范围。

1.目前实现了可以按照页数来获取测试项目以及资产。

2.可以通过修改getTarget方法中的range实现爬取哪几页的资产，默认是（1-9页）

3.在爬取的时候添加了一个随机延迟的效果，避免爬取过猛，导致被封

4.运行结束之后，即可获得一个txt文件和一个excel的表格。txt文件里面存储着本次发行的所有测试URL。Excel里面按照项目进行了分类了测试的URL。


##实现的原理
1.先请求获取每一页的数据，每一页里面存储着项目的名称以及访问项目的URL

2.根据项目的URL获取到了能够获取测试URL的一个API接口

3，请求API接口获取到所测试的URL


