# project14： Implement a PGP scheme with SM2
## 实现环境
#### 软件环境：
VSCode
#### 硬件环境：
11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz   2.69 GHz 16.0 GB (15.6 GB 可用)

## 实现方式
加密过程：
![image](https://github.com/cscs666/homework_group_81/blob/main/project14/%25S_R%7DOBJMG_%7DD%25B%7D4DJ1%24D2.png)<br>   
解密过程：
![image](https://github.com/cscs666/homework_group_81/blob/main/project14/YZ5SATBAKFGQ%60%60_XXXE%7DAPH.png)<br>   

加密时先用SM4加密信息，再用SM2加密SM4的密钥K；解密时先用SM2解密SM4的密钥K，再用K去解出明文
## 运行要求
使用python，包含gmssl，time。
## 实现效果
加密效果图：

![image](https://github.com/cscs666/homework_group_81/blob/main/project14/C26%7DV4%5D\(L%5DFX%25U44E%7DN9E%243.png)<br>  

|加密比特数|运行时间s|  
|24       |0.023995|   
|解密比特数|运行时间s|   
| 24      |0.016002|  
经测试得，PGP在不花费很多时间的前提下给出了一种较好的保护密钥的解决方案，在时间和安全性上有较好的权衡。
