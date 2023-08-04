import random
import gmssl.sm3 as SM3
import time


def rho_attack(n):
    val1=random.randbytes(n)
    val1Hash=SM3.sm3_hash(SM3.bytes_to_list(val1))#固定一个hash寻找另一个碰撞的hash
    val2HashList=[]
    for i in range(2**(n*8)):
        val2=random.randbytes(n)
        val2Hash=SM3.sm3_hash(SM3.bytes_to_list(val2))
        if val1Hash in val2HashList:
            print("找到碰撞,val1是",val1,"val2是",val2)
            return
        val2HashList.append(val2Hash)
    print("未找到碰撞")

time1=time.time()
rho_attack(2)
time2=time.time()
print("耗时",time2-time1,"s")
	

