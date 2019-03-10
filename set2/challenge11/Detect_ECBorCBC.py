from Crypto.Cipher import AES
from os import urandom
from random import randint
import collections
KEY_SIZE = 16
IV_SIZE = 16
BLOCK_SIZE = 16

def genkey(size):
	return urandom(size)

def appendbytes(pt):
	prefix = randint(5,10)
	suffix = randint(5,10)
	return str(urandom(prefix)) + str(pt) + str(urandom(suffix))

def genIV():
	return str(urandom(IV_SIZE))

def PKCS7_padding(pt):
	if len(pt)%16 == 0:
		return pt
	else:
		return pt.ljust(16*(len(pt)/16)+16,chr((16*(len(pt)/16)+16)-len(pt)))

def encrypt():
	key = genkey(KEY_SIZE)
	pt = raw_input("Data to encrypt > ")
	#pt = appendbytes(pt)
	pt = PKCS7_padding(pt)
	print pt
	iv = genIV()
	if randint(0,1) == 0:
		aes = AES.new(key, AES.MODE_ECB)
		mode = "ECB"
	else:
		aes = AES.new(key, AES.MODE_CBC, iv)
		mode = "CBC"
	ct = aes.encrypt(pt).encode("base64")
	print "Cypher text > " + str(ct) + "\nEncrypted with  > " + str(mode)
	return ct

def detect(ct):
	ct = ct.decode("base64")
	substrings = [ct[i:i + BLOCK_SIZE] for i in range(0,len(ct),BLOCK_SIZE)]
	score = len(substrings) - len(set(substrings))
	return score

def main():
	ct = encrypt()
	if detect(ct) > 0:
		print "Guessed mode > ECB"
	else:
		print "Guessed mode > CBC"
main()
