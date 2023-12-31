# project4： do your best to optimize SM3 implementation (software)
## 实现环境
#### 软件环境：
VSCode
#### 硬件环境：
11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz   2.69 GHz 16.0 GB (15.6 GB 可用)

## 实现方式
SM3密码杂凑算法是中国国家密码管理局2010年公布的中国商用密码杂凑算法标准。具体算法标准原始文本参见参考文献[1]。该算法于2012年发布为密码行业标准(GM/T 0004-2012)，2016年发布为国家密码杂凑算法标准(GB/T 32905-2016)。
SM3适用于商用密码应用中的数字签名和验证，是在SHA-256基础上改进实现的一种算法，其安全性和SHA-256相当。SM3和MD5的迭代过程类似，也采用Merkle-Damgard结构。消息分组长度为512位，摘要值长度为256位。
整个算法的执行过程可以概括成四个步骤：消息填充、消息扩展、迭代压缩、输出结果。
各个步骤的流程图与必要介绍：
##### 消息填充：
1、先填充一个“1”，后面加上k个“0”。其中k是满足(n+1+k) mod 512 = 448的最小正整数。
2、追加64位的数据长度（bit为单位，大端序存放。观察算法标准原文附录A运算示例可以推知。）

![image](https://pic3.zhimg.com/80/v2-366d5284c75a6ac92fdbc12ce5b45a2a_1440w.webp)<br>
##### 消息扩展：
SM3的迭代压缩步骤没有直接使用数据分组进行运算，而是使用这个步骤产生的132个消息字。（一个消息字的长度为32位）概括来说，先将一个512位数据分组划分为16个消息字，并且作为生成的132个消息字的前16个。再用这16个消息字递推生成剩余的116个消息字。在最终得到的132个消息字中，前68个消息字构成数列 Wj ，后64个消息字构成数列 W'j ，其中下标j从0开始计数。
##### 迭代压缩：
SM3使用消息扩展得到的消息字进行运算。这个迭代过程可以用这幅图表示：

![image](https://github.com/cscs666/homework_group_81/blob/main/project4/v2-24cede4010e3cef97ae606ff71bd0c25_1440w.webp)<br>
初值IV被放在A、B、C、D、E、F、G、H八个32位变量中。整个算法中最核心、也最复杂的地方就在于压缩函数。压缩函数将这八个变量进行64轮相同的计算，一轮的计算过程如下图所示：

![image](https://raw.githubusercontent.com/cscs666/homework_group_81/main/project4/v2-380647a6a95d50e571dca706f8022a23_1440w.webp)<br>
图中不同的数据流向用不同颜色的箭头表示。
##### 输出结果：
最后，再将计算完成的A、B、C、D、E、F、G、H和原来的A、B、C、D、E、F、G、H分别进行异或，就是压缩函数的输出。这个输出再作为下一次调用压缩函数时的初值。依次类推，直到用完最后一组132个消息字为止。
将得到的A、B、C、D、E、F、G、H八个变量拼接输出，就是SM3算法的输出。
## 运行要求
使用python语言，包含random，time库
## 实现效果
![image](https://github.com/cscs666/homework_group_81/blob/main/project4/1LREH%601\)W%5B4OLTL7%40MTK2X7.png)<br>

![image](https://github.com/cscs666/homework_group_81/blob/main/project4/V\)M%7DCI\(J%5B0VA%7B%5DDC3K04Y0M.png)<br>

## 分析
实现过程本身不算难，只需根据算法流程与流程图一步步走下去即可。在我实现的过程中，难点在于统筹各个函数输入输出的变量的类型。编程的时候经常需要byte却传了str，给编程工作带来很大的麻烦。
