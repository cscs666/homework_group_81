from gmssl import sm3, func
import mySM3#这个文件复制自gmssl中sm3的定义，并进行了一些修改让函数可以自定义iv
import struct
import os
import time


def generate_guess_hash(old_hash, secret_len, append_m):#产生一个用来猜测的hash
	vectors = []
	message = ""
	for r in range(0, len(old_hash), 8):
		vectors.append(int(old_hash[r:r + 8], 16))

	if secret_len > 64:
		for i in range(0, int(secret_len / 64) * 64):
			message += '1'
	for i in range(0, secret_len % 64):
		message += '1'
	message = func.bytes_to_list(message)
	message = padding(message)
	message.extend(func.bytes_to_list(append_m))
	return mySM3.sm3_hash(message, vectors)


def padding(msg):#分组并填充
	msglen = len(msg)
	msg.append(0x80)
	msglen += 1
	tail = msglen % 64
	range_end = 56
	if tail > range_end:
		range_end = range_end + 64#尾部填充
	for i in range(tail, range_end):
		msg.append(0x00)
	bit_len = (msglen - 1) * 8
	msg.extend([int(x) for x in struct.pack('>q', bit_len)])#长度扩展
	for j in range(int((msglen - 1) / 64) * 64 + (msglen - 1) % 64, len(msg)):
		global pad
		pad.append(msg[j])
		global pad_ms
		pad_ms += str(hex(msg[j]))
	return msg


secret = os.urandom(32)#这是随机密文
secret_hash = sm3.sm3_hash(func.bytes_to_list(secret))
secret_len = len(secret)
add_m = b"sdusdusducccssscccsss"
pad_ms = ""
pad = []
print("秘密是",secret)
print("将秘密进行sm3运算后：" + secret_hash)
print("扩展长度部分为", add_m)

time1=time.time()
guess_hash = generate_guess_hash(secret_hash, secret_len, add_m)
new_msg = func.bytes_to_list(secret)
new_msg.extend(pad)
new_msg.extend(func.bytes_to_list(add_m))
new_msg_str = secret + pad_ms.encode('utf-8') + add_m #中间的pad_ms是为了填充0
time2=time.time()

new_hash = sm3.sm3_hash(new_msg)
print("消耗时间" + str(time2-time1))
print("新的信息为\n {}".format(new_msg_str))
print("新信息的sm3值为:" + new_hash)
if new_hash == guess_hash:
	print("成功攻击")
else:
	print("失败")