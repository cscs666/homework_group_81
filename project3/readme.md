# project3： implement length extension attack for SM3, SHA256, etc.
## 实现环境
#### 软件环境：
VSCode
#### 硬件环境：
11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz   2.69 GHz 16.0 GB (15.6 GB 可用)

## 实现方式
长度扩展攻击（Length extension attacks）是指针对某些允许包含额外信息的加密散列函数的攻击手段。
该攻击适用于在消息与密钥的长度已知的情形下，所有采取了H(密钥∥消息) 此类构造的散列函数。MD5和SHA-1等基于Merkle–Damgård构造的算法均对此类攻击显示出脆弱性。注意，由于密钥散列消息认证码（HMAC）并未采取H(密钥∥消息)的构造方式，因此不会受到此类攻击的影响（如HMAC-MD5、HMAC-SHA1）。SHA-3算法对此攻击免疫。 [1]
对此类攻击脆弱的散列函数的常规工作方式是：获取输入消息，利用其转换函数的内部状态；当所有输入均处理完毕后，由函数内部状态生成用于输出的散列摘要。因而存在着从散列摘要重新构建内部状态、并进一步用于处理新数据（攻击者伪造数据）的可能性。如是，攻击者得以扩充消息的长度，并为新的伪造消息计算出合法的散列摘要。

## 运行要求
包含gmssl,struct,time,os库
## 实现效果

运行时间：0.00199s
在几乎所有情况下可以成功攻击

## 部分截图


![image](https://github.com/cscs666/homework_group_81/blob/main/project3/P%24ZQ4UOHKW22E327%25%5BPUIPA.png)<br>

## 分析
本次攻击化用了gmssl内的sm3库，并对sm3_hash函数进行了合理的修改，以让其可以自定义iv从而进行长度扩展攻击，极大地复用了代码，并且重写了分组相关的代码以更好地配合长度扩展攻击。
