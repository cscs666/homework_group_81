import random
from gmssl.sm3 import sm3_hash as SM3,bytes_to_list
from gmpy2 import invert
import socket
from hashlib import md5


def AddInPrimeField(x1,y1,x2,y2,a,p):#素域内的加法
    if x1==x2 and y1==p-y2:#无穷远点
        return False
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

def kdf(z,klen):#密钥派生
    ct=0#迭代次数
    k=''
    for i in range(klen//256+1):#上取整，这一步是为了分成每组256位的分组
        ct=ct+1
        k=k+SM3(bytes_to_list(bytes(hex(int(z+'{:032b}'.format(ct),2))[2:].encode())))#反复进行sm3运算。要先将十六进制数转为字节型在调用bytes_to_list
    k='0'*((256-(len(bin(int(k,16))[2:])%256))%256)+bin(int(k,16))[2:]
    return k[:klen]#返回前klen位

p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
Gx=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Gy=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
#上述值来自官方文档



dB=random.randint(1,n-1)
xB,yB=MultiPoint(Gx,Gy,dB,a,p)

def SM2Enc(message):
    message_hex=message.encode().hex()
    plen=len(hex(p))-2#减去的2是“0x”
    message='0'*((4-(len(bin(int(message_hex,16))[2:])%4))%4)+bin(int(message_hex,16))[2:]
    mlen=len(message)
    while 1:
        k=random.randint(1, n)
        while k==dB:#概率极小
            k=random.randint(1, n)
        x2,y2=MultiPoint(xB, yB, k, a, p)
        x2,y2='{:0256b}'.format(x2),'{:0256b}'.format(y2)
        #print("加密x2=",x2," y2=",y2)#测试
        t=kdf(x2+y2, mlen)
        if int(t,2)!=0:
            break
    x1,y1=MultiPoint(Gx, Gy, k, a, p)
    x1,y1=(plen-len(hex(x1)[2:]))*'0'+hex(x1)[2:],(plen-len(hex(y1)[2:]))*'0'+hex(y1)[2:]
    #print("加密x1=",x1," y1=",y1)#测试
    c1='04'+x1+y1
    c2=((mlen//4)-len(hex(int(message,2)^int(t,2))[2:]))*'0'+hex(int(message,2)^int(t,2))[2:]#c2=m异或t
    c3=SM3(bytes_to_list(bytes(hex(int(x2+message+y2,2))[2:].encode())))
    Cipher=c1+c2+c3
    return Cipher,c1,c2,c3#返回c1,c2,c3是为了方便解密测试，实际中不返回

def SM2Dec(c1,c2,c3,a,b,p):
    c1=c1[2:]
    x1,y1=int(c1[:len(c1)//2],16),int(c1[len(c1)//2:],16)
    if pow(y1,2,p)!=(pow(x1,3,p)+a*x1+b)%p:#验证x1y1是否在椭圆曲线上。椭圆曲线方程来自官方文档：y^2 = x^3 + ax + b。
        return False
    #print("解密x1=",x1," y1=",y1)#测试
    x2,y2=MultiPoint(x1, y1, dB, a, p)
    x2,y2='{:0256b}'.format(x2),'{:0256b}'.format(y2)
    #print("解密x2=",x2," y2=",y2)#测试
    klen=len(c2)*4
    t=kdf(x2+y2, klen)
    if int(t,2)==0:
        return False
    m='0'*(klen-len(bin(int(c2,16)^int(t,2))[2:]))+bin(int(c2,16)^int(t,2))[2:]#m=c2异或t
    u=SM3(bytes_to_list(bytes(hex(int(x2+m+y2,2))[2:].encode())))
    if u!=c3:
        return False
    return hex(int(m,2))[2:]
#####以上来自project11的sm2实现
host="127.0.0.1"
port=50589
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.connect((host,port))
    print("已连接")
except:
    print("未连接")
#####进行网络连接
d1=random.randint(1,n-1)
d1inv=invert(d1,n)
p1x,p1y=MultiPoint(Gx,Gy,d1inv,a,p)
s.sendall((str(p1x)+'\n'+str(p1y)).encode())#将P发送过去
p1x,p1y=[int(i) for i in s.recv(1024).decode().split('\n')]#接受传过来的P1
print("收到P1:",(p1x,p1y),"\n")
Z='123456789'#双方的共享身份标记
M='sdusdusducccssscccsss'#message
M_=Z+M#M'=Z||M
e=md5(bytes(M_,'utf-8')).hexdigest()
k1=random.randint(1,n-1)
Q1x,Q1y=MultiPoint(Gx,Gy,k1,a,p)
s.sendall((str(Q1x)+'\n'+str(Q1y)+'\n'+str(e)).encode())#继续按照流程图发送/接受
r,s2,s3=[int(i) for i in s.recv(1024).decode().split('\n')]
print("收到r:",r,"\ns2:",s2,"\ns3:",s3)
s_=((d1*k1)*s2+d1*s3-r)%n
if s_!=0 or s!=n-r:
    signature=(r,s_)
    print("签名为",signature)#最终展示签名
else:
    print("签名失败")