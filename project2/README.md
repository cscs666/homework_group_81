# project2： implement the Rho method of reduced SM3
## 实现环境
#### 软件环境：
VSCode
#### 硬件环境：
处理器11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz   2.69 GHz   16.0 GB (15.6 GB 可用)
## 实现方式
SM3的rho攻击是一种利用了SM3哈希函数中的rho变换特性来构造碰撞的攻击思路。因为rho攻击是对一个固定hash值的攻击，而不像生日攻击那样具有随机性。结合实验结果，我倾向于认为rho攻击要慢于生日碰撞。
rho碰撞攻击的基本思想：1.初始化两个变量 x 和 y 为相同的初始值。2.以不同的方式迭代计算 x 和 y 的哈希值，例如通过对 x 和 y 进行不同次数的哈希计算。3.在每次迭代后，比较 x 和 y 的值，如果它们相等，则找到了碰撞点，攻击成功。4.如果 x 和 y 不相等，则继续迭代计算，重复步骤2和3，直到找到碰撞点。
在这里，继续使用python语言与gmssl库。

## 运行要求
random、gmssl、time库
## 实现效果

|bytes|时间:s|
|:---|:---|
|1|0.028907|
|2|21.256989|


## 部分截图
1byte：<br>
![inage](https://github.com/jixujin64/homework-group-37/blob/main/project_2/8bits.png?raw=true)
2bytes:<br>
![image](https://github.com/jixujin64/homework-group-37/blob/main/project_2/16bits.png?raw=true)

## 分析
相对于之前的朴素的基于生日悖论碰撞攻击，rho攻击算法的速度慢了很多。
