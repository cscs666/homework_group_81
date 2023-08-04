# project11： impl sm2 with RFC6979
## 实现环境
#### 软件环境：
VSCode
#### 硬件环境：
11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz   2.69 GHz 16.0 GB (15.6 GB 可用)

## 实现方式
SM2算法是一种更先进安全的算法，采用是国密标准的椭圆曲线加密算法，在我们国家商用密码体系中被用来替换RSA算法。

## 运行要求
使用python，包含random，gmssl，gmpy2，time，binascii。
## 实现效果
加密效果图：

![image](https://github.com/cscs666/homework_group_81/blob/main/project11/Q%25QR62OEHO3%60%5BN2COXH%256%25S.png)<br>
|加密位数|运行时间s|  
|15     |0.012962|  
|10000  |2.023226|  
经过与密码算法库的实现结果进行比较，发现与密码库的加密结果一致，并且可以解密成功，证明加密算法实现正确。
