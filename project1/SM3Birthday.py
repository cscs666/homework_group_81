import random
import gmssl.sm3 as SM3
import time

def Birthday(LEN):
    valHashList=[]
    count=0
    while 1:
        val=random.randbytes(LEN)#两组随机数寻找碰撞
        valHash=SM3.sm3_hash(SM3.bytes_to_list(val))
        if valHash in valHashList:
            print("找到碰撞,寻找次数为",count)
            return count
        else:
            count+=1
            valHashList.append(valHash)

count=[]
time1=time.time()
for i in range(100):
    temp=Birthday(4)
    count.append(temp)
average=sum(count)/len(count)
time2=time.time()
print("对于2字节的数据，100次寻找碰撞的平均寻找次数为",average,"平均时间为",(time2-time1)/100,"s")
