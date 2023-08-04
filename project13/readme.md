# project13： Implement the above ECMH scheme
## 实现环境
#### 软件环境：
VSCode
#### 硬件环境：
11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz   2.69 GHz 16.0 GB (15.6 GB 可用)

## 实现方式
![image](https://github.com/Borpord/homework-group6/raw/main/Project13%3A%20Implement%20the%20above%20ECMH%20scheme/md_image/1.png)<br>  

ECMH就是某些消息的哈希值各自映射到椭圆曲线上的一个点，并使用在椭圆曲线定义下的加、点乘、取模等运算来进行信息的综合操作以方便验证。
## 运行要求
使用python，包含random，hashlib，gmpy2，math，sympy。
## 实现效果
加密效果图：

![image](https://github.com/cscs666/homework_group_81/blob/main/project13/H9G5G%7D95Z\(F%25%5DQTVTGT03T3.png)<br>  

|加密比特数|运行时间s|  
|6，8    |0.001|   
|生成密钥|运行时间s|   
         |3.462836|  
经测试得，hash过程普遍较快，运行程序的主要时间花费在生成密钥上.
