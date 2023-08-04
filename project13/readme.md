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

![image](https://github.com/cscs666/homework_group_81/blob/main/project11/Q%25QR62OEHO3%60%5BN2COXH%256%25S.png)<br>
|加密位数|运行时间s|  
|15     |0.012962|  
|10000  |2.023226|  
经过与密码算法库的实现结果进行比较，发现与密码库的加密结果一致，并且可以解密成功，证明加密算法实现正确。
