from Crypto.Cipher import AES
from os import urandom
from random import randint
from base64 import b64encode, b64decode

KEY_SIZE = 16
IV_SIZE = 16
BLOCK_SIZE = 16
PLAINTEXT_SIZE = 1337

def genkey(size):
	return urandom(size)

def appendbytes(pt):
	prefix = randint(5,10)
	suffix = randint(5,10)
	return urandom(prefix) + pt + urandom(suffix)

def genIV():
	return urandom(IV_SIZE)

def PKCS7_padding(s):
	if len(s)%BLOCK_SIZE != 0:
		return s + chr((BLOCK_SIZE*(len(s)//BLOCK_SIZE)+BLOCK_SIZE)-len(s)).encode()*((BLOCK_SIZE*(len(s)//BLOCK_SIZE + 1))-len(s))
	return s

def encrypt(pt):
	key = genkey(KEY_SIZE)
	pt = PKCS7_padding(pt)
	iv = genIV()
	if randint(0,1) == 0:
		aes = AES.new(key, AES.MODE_ECB)
		mode = "ECB"
	else:
		aes = AES.new(key, AES.MODE_CBC, iv)
		mode = "CBC"
	ct = b64encode(aes.encrypt(pt))
	return (ct,mode)

def AES_ECB_Score(ct):
	ct = b64decode(ct)
	blocks = [ct[i:i + BLOCK_SIZE] for i in range(0, len(ct), BLOCK_SIZE)]
	score = len(blocks) - len(set(blocks))
	return score

def main():
	pt = appendbytes(urandom(PLAINTEXT_SIZE))
	ct = encrypt(pt+b"A"*1337)
	print ("Ciphertext > " + str(ct[0]) + "\nAES mode used > " + str(ct[1]))
	if AES_ECB_Score(ct[0]) > 0:
		print ("Guessed mode > ECB")
	else:
		print ("Guessed mode > CBC")

if __name__ == '__main__':
	main()
