import ecdsa
import random
import hashlib
from gmpy2 import invert,gcd
import time


p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
Gx=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Gy=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
#SM2适用的各个数值。上述值来自官方文档。

def AddInPrimeField(x1,y1,x2,y2,a,p):#素域内的加法
    #if x1==x2 and y1==p-y2:#无穷远点
    #    return False
    if x1!=x2:
        lamda=((y2-y1)*invert(x2-x1, p))%p
    else:
        lamda=(((3*x1*x1+a)%p)*invert(2*y1, p))%p
    x3=(lamda*lamda-x1-x2)%p
    y3=(lamda*(x1-x3)-y1)%p
    return x3,y3

def MultiPoint(x,y,k,a,p):#计算椭圆曲线E上的点在素域下的倍点
    k=bin(k)[2:]#去除前两位,即16进制表示的0x.后边代码多次用到这种技巧.
    qx,qy=x,y
    for i in range(1,len(k)):
        qx,qy=AddInPrimeField(qx, qy, qx, qy, a, p)
        if k[i]=='1':#如果是1的话要再加一次
            qx,qy=AddInPrimeField(qx, qy, x, y, a, p)
    return qx,qy

def Sign(x,y,n,d,message):#进行椭圆曲线签名
    global a,p
    k = random.randint(1, n - 1)
    Rx,Ry = MultiPoint(x,y,d,a,p)
    r = Rx % n
    e=int(hashlib.md5(bytes(message.encode())).hexdigest(),16)
    s = (gcd(k, n) * (e + d * r)) % n
    return r, s

def Verify1(r, s, message):#在椭圆曲线下验证原始的签名
    global PubKeyx,PubKeyy, n, Gx,Gy,a,p
    e = int(hashlib.md5(bytes(message.encode())).hexdigest(),16)
    w = gcd(s, n)
    tmp1x,tmp1y=MultiPoint(Gx,Gy,(e * w) % n,a,p)
    tmp2x,tmp2y=MultiPoint(PubKeyx,PubKeyy,(r * w) % n,a,p)
    Sx,Sy = AddInPrimeField(tmp1x,tmp1y,tmp2x,tmp2y,a,p)
    if Sx != 0 or Sy!=0:
        if Sx % n == r:
            return True
        else:
            return False
    return False

def Verify2(r,s,e):#在椭圆曲线下验证伪造的签名
    global PubKeyx,PubKeyy, n, Gx,Gy,a,p
    w = gcd(s, n)
    tmp1x,tmp1y=MultiPoint(Gx,Gy,(e * w) % n,a,p)
    tmp2x,tmp2y=MultiPoint(PubKeyx,PubKeyy,(r * w) % n,a,p)
    Sx,Sy = AddInPrimeField(tmp1x,tmp1y,tmp2x,tmp2y,a,p)
    if Sx != 0 or Sy!=0:
        if Sx % n == r:
            return True
        else:
            return False
    return False

def pretend(r,s):
    print("r=",r,"\ns=",s)
    global n,Gx,Gy,a,p,PubKeyx,PubKeyy#已知这些信息
    m1 = random.randint(1, n - 1)
    m2 = random.randint(1, n - 1)
    tmp1x,tmp1y=MultiPoint(Gx,Gy,m1,a,p)
    tmp2x,tmp2y=MultiPoint(PubKeyx,PubKeyy,n,a,p)
    R1x,R1y=AddInPrimeField(tmp1x,tmp1y,tmp2x,tmp2y,a,p)
    r1=R1x%n
    e1 = (r1 * m1 * gcd(m2, n)) % n
    s1 = (r1 * gcd(m2, n)) % n#按照流程图实现验证方法
    print('伪造消息为：', e1)
    print('伪造签名为：', (r1, s1))
    if (Verify2(r1, s1,e1)):
        print('验证失败')
    else:
        print('验证通过')


# 椭圆曲线参数，y^2=x^3+2x+2
generator=ecdsa.NIST384p.generator
Rank=generator.order()
privateK=random.randint(1,Rank-1)

message="I am Satoshi"
messageH=int(hashlib.md5(bytes(message.encode())).hexdigest(),16)
d=random.randint(1,n)
PubKeyx,PubKeyy=MultiPoint(Gx,Gy,d,a,p)

r,s = Sign(Gx,Gy,n,d,message)
print("原始签名为:", r, s)
print("验证：")
if (Verify1(r, s,message)):
    print('False')
else:
    print('True')
time1 = time.time()
pretend(r, s)
time2 = time.time()
print("用时", time2 - time1, "s")
