# project15：implement sm2 2P sign with real network communication  
## 实现环境
#### 软件环境：
VSCode
#### 硬件环境：
11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz   2.69 GHz 16.0 GB (15.6 GB 可用)

## 实现方式
整个签名过程：
![image](https://github.com/Borpord/homework-group6/raw/main/Project15%3A%20implement%20sm2%202P%20sign%20with%20real%20network%20communication/md_image/1.png)<br>   

SM2 两方协作是指网络中的两方分别生成两个子密钥，共同构建公钥和私钥，参与到同一个签名生成的过程当中来。
在具体实现时，我们假设左边的人是client，右边的人是server。

## 运行要求
使用python，包含gmssl，socket，hashlib，random，gmpy2。
## 实现效果
客户方效果图：

![image](https://github.com/cscs666/homework_group_81/blob/main/project15/ADZ%5D9T\)J\(Q7KG61NM%24HR%7DIQ.png)<br>  

服务方效果图：
![image](https://github.com/cscs666/homework_group_81/blob/main/project15/TN2\(II%7DYC%5D4E9LD5G~MR\(6H.png)<br>  
