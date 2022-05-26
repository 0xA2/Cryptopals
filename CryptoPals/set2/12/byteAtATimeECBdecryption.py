from Crypto.Cipher import AES
from os import urandom

import base64

def padding(string, blockSize):
	if len(string)%blockSize == 0:
		return string.encode() + b'\x16'
	byte = blockSize-(len(string)%blockSize)
	pad = b"".join( bytes.fromhex( hex(byte)[2:].rjust(2,"0") ) for _ in range(byte))
	return string.encode() + pad

def encryptionOracle(userInput, key):
	plaintext = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK").decode()
	pt = padding(userInput + plaintext, 16)
	aes = AES.new(key, AES.MODE_ECB)
	ciphertext = aes.encrypt(pt)
	return ciphertext

def bruteForceECB(key, numOfBlocks):
	plaintext = ""
	for i in range(1, 16*numOfBlocks):
		cur = encryptionOracle("A"*(16*numOfBlocks - i), key)[:(16*numOfBlocks)]
		for j in range(0,128):
			if encryptionOracle("A"*(16*numOfBlocks - i) + plaintext + chr(j), key)[:(16*numOfBlocks)] == cur:
				plaintext += chr(j)
				break
	return plaintext

def main():
	key = urandom(16)
	print (bruteForceECB(key,9))

if __name__ == "__main__":
	main()
