import random
import time

bytes_to_list = lambda data: [i for i in data]#将比特流转换为数字数组

LeftShift= lambda x, n:((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)#上两个是循环移位和将字节转化为列表，是现有定义
IV = [
    1937774191, 1226093241, 388252375, 3666478592,
    2842636476, 372324522, 3817729613, 2969243214,
]

T_j = [
    2043430169, 2043430169, 2043430169, 2043430169, 2043430169, 2043430169,
    2043430169, 2043430169, 2043430169, 2043430169, 2043430169, 2043430169,
    2043430169, 2043430169, 2043430169, 2043430169, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042
]#定值

def ff(x, y, z, j):#完成ff布尔表达式的内容
    if 0 <= j and j < 16:
        r = x ^ y ^ z
    elif 16 <= j and j < 64:
        r = (x & y) | (x & z) | (y & z)
    return r

def gg(x, y, z, j):#完成gg布尔表达式的内容
    if 0 <= j and j < 16:
        r = x ^ y ^ z
    elif 16 <= j and j < 64:
        r = (x & y) | ((~ x) & z)
    return r

def p0(x):#实现置换p0
    return x ^ (LeftShift(x, 9 % 32)) ^ (LeftShift(x, 17 % 32))

def p1(x):#实现置换p1
    return x ^ (LeftShift(x, 15 % 32)) ^ (LeftShift(x, 23 % 32))

def cf(v_i, b_i):#消息扩展与压缩
    w = []
    for i in range(16):
        weight = 0x1000000
        data = 0
        for k in range(i*4,(i+1)*4):
            data = data + b_i[k]*weight
            weight = int(weight/0x100)
        w.append(data)

    for j in range(16, 68):
        w.append(0)
        w[j] = p1(w[j-16] ^ w[j-9] ^ (LeftShift(w[j-3], 15 % 32))) ^ (LeftShift(w[j-13], 7 % 32)) ^ w[j-6]
    w_1 = []
    for j in range(0, 64):
        w_1.append(0)
        w_1[j] = w[j] ^ w[j+4]
    #以上是对传入的消息分组的处理与扩展
    a, b, c, d, e, f, g, h = v_i#初始iv里的8个数字被放在这八个变量中进行计算

    for j in range(0, 64):#依据sm3的运算法则进行64轮运算以进行压缩
        ss_1 = LeftShift(
            ((LeftShift(a, 12 % 32)) +
            e +
            (LeftShift(T_j[j], j % 32))) & 0xffffffff, 7 % 32
        )
        ss_2 = ss_1 ^ (LeftShift(a, 12 % 32))
        tt_1 = (ff(a, b, c, j) + d + ss_2 + w_1[j]) & 0xffffffff
        tt_2 = (gg(e, f, g, j) + h + ss_1 + w[j]) & 0xffffffff
        d = c
        c = LeftShift(b, 9 % 32)
        b = a
        a = tt_1
        h = g
        g = LeftShift(f, 19 % 32)
        f = e
        e = p0(tt_2)

        #a, b, c, d, e, f, g, h = map(
         #   lambda x:x & 0xFFFFFFFF ,[a, b, c, d, e, f, g, h])

    v_j = [a, b, c, d, e, f, g, h]
    return [v_j[i] ^ v_i[i] for i in range(8)]#把这八个变量拼接输出就是压缩函数的输出

def sm3(msg):#输入需为字节型
    #print(msg)
    len1 = len(msg)
    reserve1 = len1 % 64
    msg.append(0x80)
    reserve1 = reserve1 + 1
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64

    for i in range(reserve1, range_end):
        msg.append(0x00)#消息填充

    len2 = (len1) * 8
    len2str = [len2 % 0x100]
    for i in range(7):
        len2 = int(len2 / 0x100)
        len2str.append(len2 % 0x100)
    for i in range(8):
        msg.append(len2str[7-i])

    NumofGroups = round(len(msg) / 64)

    B = []#消息分组
    for i in range(0, NumofGroups):
        B.append(msg[i*64:(i+1)*64])#给消息分的组

    V = []
    V.append(IV)
    for i in range(0, NumofGroups):
        V.append(cf(V[i], B[i]))

    y = V[i+1]
    result = ""
    for i in y:
        result = '%s%08x' % (result, i)
    return result


secret=b'202100460066cccssscccsss'
print("秘密为",secret)
time1=time.time()
res=sm3(bytes_to_list(secret))
time2=time.time()
print("hash结果为：",res,"\n花费时间为",time2-time1)


secret=random.randbytes(8192)
time1=time.time()
res=sm3(bytes_to_list(secret))
time2=time.time()
print("随机8192位字节流hash结果为：",res,"\n花费时间为",time2-time1)