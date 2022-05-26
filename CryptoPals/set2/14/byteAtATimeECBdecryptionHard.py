from Crypto.Cipher import AES
from os import urandom
from random import randint

import base64

BLOCKSIZE = 16
key = urandom(BLOCKSIZE)
randomPrefix = urandom(randint(0,255))

def padding(string, blockSize):
	if len(string)%blockSize == 0:
		return string + '\x16'*16
	byte = blockSize-(len(string)%blockSize)
	pad = b"".join( bytes.fromhex( hex(byte)[2:].rjust(2,"0") ) for _ in range(byte))
	return string + pad

def encryptionOracle(userInput):
	plaintext = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
	pt = padding( randomPrefix + userInput + plaintext, BLOCKSIZE)
	aes = AES.new(key, AES.MODE_ECB)
	ciphertext = aes.encrypt(pt)
	return ciphertext

def getBlocks(ciphertext):
	ret = []
	for i in range(0,len(ciphertext)//BLOCKSIZE):
		ret.append(ciphertext[i*BLOCKSIZE:(i+1)*BLOCKSIZE])
	return ret

def getPrefixLen():
	length = 0
	while(True):
		flag = b"A"*(32+length)
		curTry = encryptionOracle(flag)
		curBlocks = getBlocks(curTry)
		for i in range(0,(len(curBlocks)-1)):
			if curBlocks[i] == curBlocks[i+1]:
				return length, i*BLOCKSIZE
		length += 1

def bruteForceECBhard(numOfBlocks, ciphertextPrefix, prefixBlocks):
	plaintext = b""
	for i in range(1, BLOCKSIZE*numOfBlocks):
		cur = encryptionOracle(b"A"*ciphertextPrefix + b"A"*(BLOCKSIZE*numOfBlocks - i))[prefixBlocks:][:BLOCKSIZE*numOfBlocks]
		for j in range(0,128):
			if encryptionOracle(b"A"*ciphertextPrefix + b"A"*(BLOCKSIZE*numOfBlocks - i) + plaintext + chr(j).encode() )[prefixBlocks:][:BLOCKSIZE*numOfBlocks] == cur:
				plaintext += chr(j).encode()
				break
	return plaintext.decode()

def main():
	ciphertextPrefix, prefixBlocks = getPrefixLen()
	print (bruteForceECBhard(9, ciphertextPrefix, prefixBlocks))

if __name__ == "__main__":
	main()
