import base64
import binascii

from Crypto.Cipher import AES
from math import ceil

BLOCK_SIZE = 16

def xorBytes(data0, data1):
	ret = b"".join(binascii.unhexlify(hex(data0[i]^data1[i])[2:].encode().rjust(2,b'0')) for i in range(min(len(data0),len(data1))))
	return ret

def decrypt(ct,key,nonce):
	aes = AES.new(key, AES.MODE_ECB)
	keystream = b"".join(aes.encrypt(nonce+chr(ord(str(counter))-48).ljust(8,'\x00').encode()) for counter in range(ceil(len(ct)/BLOCK_SIZE)))
	return xorBytes(ct,keystream)

def main():
	ct = base64.b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
	key = b'YELLOW SUBMARINE'
	nonce = b'\x00'*8
	print (decrypt(ct,key,nonce).decode())

if __name__ == "__main__":
	main()
