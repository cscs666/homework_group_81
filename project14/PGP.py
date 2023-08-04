import gmssl.sm2 as SM2
import gmssl.sm4 as SM4
import time

def sm4_encode(key, data):
    sm4Alg = SM4.CryptSM4()  # 实例化sm4
    sm4Alg.set_key(key.encode(), SM4.SM4_ENCRYPT)  # 设置密钥
    dateStr = str(data)
    print("SM4明文:", dateStr)
    enRes = sm4Alg.crypt_ecb(dateStr.encode())  # 开始加密,bytes类型，ecb模式
    enHexStr = enRes.hex()
    print("SM4密文:", enHexStr)
    return enHexStr # 返回十六进制值


def sm4_decode(key, data):
    sm4Alg = SM4.CryptSM4()  # 实例化sm4
    sm4Alg.set_key(key.encode(), SM4.SM4_DECRYPT)  # 设置密钥
    deRes = sm4Alg.crypt_ecb(bytes.fromhex(data))  # 开始解密。十六进制类型,ecb模式
    deHexStr = deRes.decode()
    print("SM4解密后明文:", deRes);
    return deHexStr

def sender(message):
    K=b"0123456789ABCDEF"
    cipherM=sm4_encode(str(K),message)#先用SM4加密信息
    #一对可行的密钥对
    pk,sk='00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5','B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    SM2Object=SM2.CryptSM2(pk,sk)
    cipherK=SM2Object.encrypt(K)#再用sm2加密密钥
    return cipherK,cipherM,pk,sk

def receiver(cipherK,cipherM,pk,sk):
    SM2Object=SM2.CryptSM2(pk,sk)
    K=SM2Object.decrypt(cipherK)#先用SM2解密密钥
    M=sm4_decode(str(K),cipherM)#再用SM4解出明文
    return M


message="sdusdusdusducccssscccsss"
time1=time.time()
cipherK,cipherM,pk,sk=sender(message)
time2=time.time()
print("cipherK=",cipherK,"\ncipherM=",cipherM,"加密耗时",time2-time1)
time1=time.time()
M=receiver(cipherK,cipherM,pk,sk)
time2=time.time()
print("M=",M,"解密耗时",time2-time1)
