from Crypto.Cipher import AES
from base64 import b64decode
from os import urandom
from random import randint

import string

BLOCKSIZE = 16

def getRandomString():
	strings = ["MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=","MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=","MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==","MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==","MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl","MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==","MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==","MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=","MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=","MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]
	return b64decode(strings[randint(0,len(strings)-1)])


def padding(string, blockSize):
	if len(string)%blockSize == 0:
		return string + b'\x0f'*16
	byte = blockSize-(len(string)%blockSize)
	pad = b"".join( bytes.fromhex( hex(byte)[2:].rjust(2,"0") ) for _ in range(byte))
	return string + pad


def PKCS7paddingValidation(string, blocksize):
	byteNum = string[len(string)-1]
	toVerify = string[-byteNum:]
	if toVerify == chr(byteNum).encode()*byteNum:
		return True
	return False

# Retrieve the padding used in the orignal plaintext
def getOriginalPadding(lastBlock, key, previousBlock):
	editBlock = bytearray(previousBlock)
	ret = 0
	while cbcDecrypt(lastBlock, key, editBlock):
		editBlock[ret+1] = 255
		ret += 1
	return chr(BLOCKSIZE - ret).encode()

# Get list of ciphertext blocks
def getBlocks(ciphertext):
	ret = []
	for i in range(0,len(ciphertext)//BLOCKSIZE):
		ret.append(ciphertext[i*BLOCKSIZE:(i+1)*BLOCKSIZE])
	return ret


def cbcEncrypt(plaintext, key, iv):
	plaintext = padding(plaintext, BLOCKSIZE)
	aes = AES.new(key, AES.MODE_CBC, iv)
	ciphertext = aes.encrypt(plaintext)
	return ciphertext


def cbcDecrypt(ciphertext, key, iv):
	aes = AES.new(key, AES.MODE_CBC, iv)
	plaintext = aes.decrypt(ciphertext)
	return PKCS7paddingValidation(plaintext, BLOCKSIZE)


def cbcPaddingOracleAttack(ciphertext, key, iv):
	plaintext = b""
	blocks = getBlocks(ciphertext)
	blocks.insert(0,iv)

	# We'll need this later for solving ambiguities
	originalPadding = getOriginalPadding(blocks[ len(blocks)-1  ], key, blocks[ len(blocks)-2  ])

	for i in range(0, len(blocks)-1):

		chunk = b""

		for j in range(0,BLOCKSIZE):
			curBlock = bytearray(blocks[i])
			if len(chunk) != 0:
				tmp = BLOCKSIZE - 1
				for ch in range(0, len(chunk)):
					curBlock[tmp] = (len(chunk)+1) ^ chunk[ch] ^ curBlock[tmp]
					tmp -= 1

			options = []
			for k in range(0,256):
				curBlock[len(curBlock)-1-j] = k
				if cbcDecrypt( bytearray(blocks[i+1]), key, curBlock):
					options.append(k)

			if len(options) == 1:
				chunk += chr( options[0] ^ (len(chunk)+1) ^ blocks[i][BLOCKSIZE-1-j] ).encode()
			else:
				nextChar = b""
				for op in options:
						curChar = chr( op ^ (len(chunk)+1) ^ blocks[i][BLOCKSIZE-1-j] ).encode()
						if curChar == originalPadding:
							nextChar = curChar
				chunk += nextChar

		plaintext += chunk[::-1]

	return plaintext


def main():

	key = urandom(BLOCKSIZE)
	iv = urandom(BLOCKSIZE)

	string = getRandomString()
	ciphertext = cbcEncrypt(string, key, iv)
	plaintext = cbcPaddingOracleAttack(ciphertext, key, iv)
	print ("Original plaintext:", string)
	print ("Decryption result:", plaintext)

if __name__ == "__main__":
	main()
