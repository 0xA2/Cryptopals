from Crypto.Cipher import AES
from os import urandom
from random import randint
from base64 import b64encode, b64decode

BLOCKSIZE = 16

def genkey(size):
	return urandom(size)

def appendbytes(pt):
	prefix = randint(5,10)
	suffix = randint(5,10)
	return urandom(prefix) + pt + urandom(suffix)

def genIV():
	return urandom(BLOCKSIZE)

def PKCS7Padding(string, blockSize):
	if len(string)%blockSize == 0:
		return string + b'\x16'*16
	byte = blockSize-(len(string)%blockSize)
	pad = b"".join( bytes.fromhex( hex(byte)[2:].rjust(2,"0") ) for _ in range(byte))
	return string + pad


def encrypt(pt):
	key = genkey(BLOCKSIZE)
	pt = PKCS7Padding(pt, BLOCKSIZE)
	iv = genIV()
	if randint(0,1) == 0:
		aes = AES.new(key, AES.MODE_ECB)
		mode = "ECB"
	else:
		aes = AES.new(key, AES.MODE_CBC, iv)
		mode = "CBC"
	ct = b64encode(aes.encrypt(pt))
	return (ct,mode)

def AESECBScore(ct):
	ct = b64decode(ct)
	blocks = [ct[i:i + BLOCKSIZE] for i in range(0, len(ct), BLOCKSIZE)]
	score = len(blocks) - len(set(blocks))
	return score

def main():
	pt = appendbytes(urandom(256))
	ct = encrypt(pt+b"A"*1337)
	print ("Ciphertext > " + str(ct[0]) + "\nAES mode used > " + str(ct[1]))
	if AESECBScore(ct[0]) > 0:
		print ("Guessed mode > ECB")
	else:
		print ("Guessed mode > CBC")

if __name__ == '__main__':
	main()
