from Crypto.Cipher import AES
from Crypto.Util import Counter

import base64

BLOCKSIZE = 16

def xorStrings(data0, data1):
	ret = b"".join(bytes.fromhex(hex(data0[i]^data1[i])[2:].rjust(2,'0')) for i in range(min(len(data0),len(data1))))
	return ret

def encrypt(plaintext, key, nonce):
	aes = AES.new(key, AES.MODE_ECB)
	counter = 0
	keyStream = b""
	keyLen = (len(plaintext)//BLOCKSIZE) + 1 if len(plaintext)%16 != 0 else (len(plantext)//BLOCKSIZE)
	for i in range(0, keyLen):
		curCounter = bytes.fromhex(hex(counter)[2:(BLOCKSIZE+2)].rjust(BLOCKSIZE,'0'))[::-1]
		keyStream += aes.encrypt(nonce + curCounter)
		counter += 1
	return xorStrings(plaintext, keyStream)

def decrypt(ciphertext, key, nonce):
	aes = AES.new(key, AES.MODE_ECB)
	counter = 0
	keyStream = b""
	keyLen = (len(ciphertext)//BLOCKSIZE) + 1 if len(ciphertext)%16 != 0 else (len(ciphertext)//BLOCKSIZE)
	for i in range(0, keyLen):
		curCounter = bytes.fromhex(hex(counter)[2:(BLOCKSIZE+2)].rjust(BLOCKSIZE,'0'))[::-1]
		keyStream += aes.encrypt(nonce + curCounter)
		counter += 1
	return xorStrings(ciphertext, keyStream)

def main():
	key = b"YELLOW SUBMARINE"
	nonce = b'\x00'*(BLOCKSIZE//2)
	ciphertext = base64.b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")
	plaintext = decrypt(ciphertext, key, nonce)
	print ( plaintext.decode() )

if __name__ == "__main__":
	main()
