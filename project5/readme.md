# project5： Impl Merkle Tree following RFC6962
## 实现环境
#### 软件环境：
VSCode
#### 硬件环境：
11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz   2.69 GHz 16.0 GB (15.6 GB 可用)

## 实现方式
Merkle树的整体架构可以用一张简明易懂的图来表示：
![image](https://img-blog.csdnimg.cn/img_convert/28ddd68a529963ca7ed1d43d1c6a799a.png)<br>
以比特币中使用的二叉Merkle树为例，每条交易的哈希值就是一个叶子节点，从下往上将两个相邻叶子节点的组合哈希作为新的哈希值，新的哈希值成为树节点继续与相邻的树节点组合成新的哈希值。 

在重复一定次数后直到形成唯一的根节点。最后得到的Merkle根需要保存到区块头中，以便仅需通过区块头就可以对交易进行简单支付验证，这一过程也成为SPV（Simplified Payment Verification）。  

对于Merkle树而言，并不需要知道整棵Merkle树中每个节点的值，可以通过节点的值、Merkle根的值和相关路径来快速验证该节点是否属于该Merkle树，从而快速验证该区块中是否包含了某条交易。   

此外，时间戳用于标记区块顺序。时间戳表示自格林威治时间 1970 年 1 月 1 日 0 时 0 分 0 秒到当前时刻的总秒数，是一种完整且可验证的电子证据，能够为某一数据提供特定时间点的存在性证明。 

区块链根据时间戳的先后顺序通过链式结构将一个个区块关联起来，因此篡改区块数据的难度以时间的指数倍增加，区块链越长篡改难度就越高，这也是确保区块链不可更改性的重要因素之一。   

## 运行要求
使用python语言，包含hashlib，time库。
## 实现效果
创建2，3层的Merkel树并向内部添加数据效果图：

![image](https://github.com/cscs666/homework_group_81/blob/main/project5/K%24X%60ZIEL\)S1F%60%7BMX9G1_GV0.png)<br>

![image](https://github.com/cscs666/homework_group_81/blob/main/project5/%40D_4NSC_B_NV%252SLBVNUK%408.png)<br>

创建15层Merkel树所花费的时间为1.625559s

![image](https://github.com/cscs666/homework_group_81/blob/main/project5/%7B47%5D8NXPRNTS013_LIO%40LWV.png)<br>

## 分析与创新点

对于Merkel树而言，它的整体架构与其他的树形结构没有太大的区别，但是它与其它树形结构有很不同的一点：在寻找某个节点时需要自上而下寻找，而在改变叶子结点的数据时需要自下而上对所有沿途节点进行数据更新。  
所以，我在Merkel树的节点类中加了一个parent变量用来标记父节点，相应的增删操作也有很大不同。但这会让溯源操作变得十分简便，也节省了不少自上而下寻找的时间。
