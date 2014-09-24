## 笔试经过

### 爬虫题目

抓[22MM](http://www.22mm.cc)，没打开网站的时候，看到第一条吓尿，排除非相关，以为要用各种高大上的图像识别来排除其他。

##### 分析网站页面

浏览一圈之后，发现子网页都在`/mm/*`底下，可用正则爬完整过网站页面并避免伤及无辜。所有链接都用set去重。
	
##### 分析目标链接

要找的图应该都是大图都在类似`http://www.22mm.cc/mm/bagua/PiabPPHimiaCPaHi.html`的网页。首页和分类导航的小图应该都是imagemagick之类生成的，链接如同：`http://bgimg1.meimei22.com/big/bagua/2014-9-1/1/5887970720140820203734093_640.jpg`。其中的`big`要转换为`pic`，可能是站长防爬。

##### 参数处理
	
argparse添加参数，会自动生成帮助	

##### 线程池

threadpool控制线程池数量，但程序退出比较暴力，达到limit就exit。

##### 关于复用
我将`base_url, sub_url, pic_url`三个参数弄成全局，其中后两个是正则，但是具体网址的话可能还是会略有改动，比如目标链接的改动。

##### 改进

爬图的网页最末张包含所有链接，可以减少读取网页次数。  
urllib.urlopen的异常超时以及retries。  
（吐槽：这家网站为什么要被knowsec用来做演练，站长好可年）

### 测试题目

infix2postfix，请原谅我的孤陋，Google出来了[Shunting-yard](https://en.wikipedia.org/wiki/Shunting-yard_algorithm#The_algorithm_in_detail)。中文[wiki](http://zh.wikipedia.org/wiki/%E8%B0%83%E5%BA%A6%E5%9C%BA%E7%AE%97%E6%B3%95)也有相应算法描述，依样画瓢。

主要对象是二元运算符，可自行添加符号，注意其优先级和结合方向即可。

测试主要使用assertEqual。


