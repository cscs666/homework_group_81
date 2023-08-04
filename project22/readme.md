# project22：research report on MPT
## 实现环境
#### 软件环境：
VSCode
#### 硬件环境：
11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz   2.69 GHz 16.0 GB (15.6 GB 可用)

## 实现
为了更好地理解默克尔树、前缀树、MPT树之间的区别与联系，我决定参考两篇博客对MPT树的介绍自行实现一遍MPT树。代码附在项目文件夹里，以下是运行结果。研究报告在运行结果下方。  
其中，在代码内也有大量注释展示了我的研究过程。代码的注释大多数聚焦于各种操作该如何实现。
![image](https://github.com/cscs666/homework_group_81/blob/main/project22/E2Y~%24B%5D%40MGEB9EM\)O_M5PXU.png)<br>  

## 研究报告
### 概述
Merkle Patricia Tree（又称为Merkle Patricia Trie）是一种经过改良的、融合了Merkle tree和前缀树两种树结构优点的数据结构，是以太坊中用来组织管理账户数据、生成交易集合哈希的重要数据结构。

MPT树有以下几个作用：

1.存储任意长度的key-value键值对数据，符合以太坊的state模型；
2.提供了一种快速计算所维护数据集哈希标识的机制；
3.提供了快速状态回滚的机制；
4.提供了一种称为默克尔证明的证明方法，进行轻节点的扩展，实现简单支付验证；

### MPT树节点类型

MPT树的节点有以下4种类型：
#### 空节点
简单的表示空，在代码中是一个空串。
#### 叶子节点（Leaf Node）
表示为 [key,value]的一个键值对，其中key是key的一种特殊十六进制编码(MP编码)， value是value的RLP编码。没有子节点。
#### 分支节点（Branch Node）：
因为MPT树中的key被编码成一种特殊的16进制的表示，再加上最后的value，所以分支节点是一个 长度为17的list ** ** ， 前16个元素对应着key中的16个可能的十六进制字符 ， 如果有一个[key,value]对在这个分支节点终止，最后一个元素代表一个值 ，即分支节点既可以搜索路径的终止也可以是路径的中间节点。
可以有多个子节点。
#### 扩展节点（Extension Node）：
也是[key，value]的一个键值对 ，但是这里的 value是其他节点的hash值 ，这个 hash可以被用来查询数据库中的节点。也就是说通过hash链接到其他节点。只能有一个子节点。

### MPT树结构
简单的结构如下：
![image](https://github.com/Borpord/homework-group6/raw/main/Project22%3A%20research%20report%20on%20MPT/md_image/2.png)<br>  

### MPT树的增/删/改操作
详见实现代码
### MPT树的核心思想
该树的最主要目的是为了让hash可以还原出节点上的数据，这样只需要保存一个root(hash)，即可还原出完整的树结构，同时还可以按需展开节点数据。  
对于下图的结构而言
![image](https://pic1.zhimg.com/80/v2-345a4e2896e9605aea982b206dcbd940_1440w.webp)
比如如果只需要访问<a771355, 45>这个数据，只需展开h00, h10, h20, h30这四个hash对应的节点,大大节省了操作时间。


