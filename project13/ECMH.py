from hashlib import md5
import math
import random
from gmpy2 import invert
from sympy.ntheory.residue_ntheory import nthroot_mod#求解二次剩余

def ECCMod(a, n):  
    if math.isinf(a):
        return float('inf')
    else:
        return a % n


def ECCModMul(a, b, n):#计算椭圆曲线下的a*b^(-1) mod n
    if b == 0:
        r = float('inf')
    elif a == 0:
        r = 0
    else:
        t = bin(n - 2)[2:]
        y = 1
        i = 0
        while i < len(t):  
            y = (y ** 2) % n 
            if t[i] == '1':
                y = (y * b) % n
            i += 1
        r = (y * a) % n
    return r

def ECCAdd(x1,y1,x2,y2,a,p):#素域内的加法
    if (math.isinf(x1) or math.isinf(y1)) and (~math.isinf(x2) and ~math.isinf(y2)):  
        x3=x2
        y3=y2
    elif (~math.isinf(x1) and ~math.isinf(y1)) and (math.isinf(x2) or math.isinf(y2)): 
        x3=x1
        y3=y1
    elif (math.isinf(x1) or math.isinf(y1)) and (math.isinf(x2) or math.isinf(y2)):  
        x3=float('inf')
        y3=float('inf')#几种无穷远点的情况
    else:
        if x1!=x2 or y1!=y2:
            l = ECCModMul(y2 - y1, x2 - x1, p)
        else:
            l = ECCModMul(3 * x1 ** 2 + a, 2 * y1, p)
        x3 = ECCMod(l ** 2 - x1 - x2, p)
        y3 = ECCMod(l * (x1 - x3) - y1, p)
    return x3,y3

def MultiPoint(x,y,k,a,p):#计算椭圆曲线E上的点在素域下的倍点
    k2=bin(k)[2:]#去除前两位,即16进制表示的0x.后边代码多次用到这种技巧.
    lenk=len(k2)-1
    qx,qy=x,y
    if lenk>0:
        k=k-2**lenk
        while lenk>0:
            qx,qy=ECCAdd(qx,qy,qx,qy,a,p)
            lenk-=1
        if k>0:
            tmp1,tmp2=MultiPoint(k,x,y,a,p)
            qx,qy=ECCAdd(qx,qy,tmp1,tmp2,a,p)
    return qx,qy

#密钥生成
def keygen(a, p, n, x, y):
    #私钥d
    d = random.randint(1, n - 2)
    #公钥k
    k = MultiPoint(x,y,d,a,p)#[x,y]的d倍点作为公钥
    return d, k

def hash(message,a,b,p):
    resultx=float("inf")
    resulty=float("inf")
    for k in message:
        kHash=int(md5(k).hexdigest(),16)
        temp=ECCMod(kHash**2+a*kHash+b,p)
        y=nthroot_mod(temp,2,p)
        resultx,resulty=ECCAdd(resultx,resulty,kHash,y,a,p)
        return resultx,resulty
    
p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
Gx=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Gy=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0

privateKey,publicKey=keygen(a,p,n,Gx,Gy)
print('privateKey=',privateKey)
print('publicKey=',publicKey)
message1,message2=b"sdusdu",b"ccccssss"
res=hash((message1,message2),a,b,p)
print("信息为",(message1,message2))
print("结果为",res)
