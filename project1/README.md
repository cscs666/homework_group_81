# Project1:  
implement the naïve birthday attack of reduced SM3
## 实现环境
#### 软件环境：VSCode
#### 硬件环境:处理器	11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz   2.69 GHz   16.0 GB (15.6 GB 可用)
## 实现方式：
SM3是一种密码哈希函数，MD结构，长度小于2^64bit的消息,消息分组为512-bit，中间链接变量为256-bit，杂凑值为256-bit,.消息填充同SHA-256。使用python内置的gmssl国密算法开源库，构造碰撞问题：在生日攻击中，我们需要找到两个不同的消息，它们的哈希值相同。通过构造碰撞问题，我们可以寻找两个不同的输入消息，它们的哈希为目标哈希值。穷尽搜索：采用暴力穷尽搜索的方式，生成大量的随机消息，并计算它们的哈希值。比较这些哈希值，找到两个不同的消息，它们的哈希值相同。
## 时间和空间复杂度
生日攻击的成功与否取决于哈希函数的哈希值位数和生日悖论。SM3哈希函数输出为256位，因此攻击的时间和空间复杂度都较高，复杂度为O(2^n/2)
## 效果
逐渐增大比特，并记录随机生成两个不同的消息的次数
|bytes|run time |探索次数|
|:---|:---|:---|
|1|0.034084s|18.68|
|2|0.513412s|323.71|

## 运行截图
![image](https://github.com/jixujin64/homework-group-37/blob/main/project_1/8bit.png "8bit运行截图")<br>
![image](https://github.com/jixujin64/homework-group-37/blob/main/project_1/16bit.png?raw=true "16bit运行截图")
