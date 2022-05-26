from Crypto.Cipher import AES
from os import urandom

import base64

BLOCKSIZE = 16

def append(plaintext, prefix, suffix):
	plaintext = plaintext.replace(b";", b"").replace(b"=",b"")
	return prefix + plaintext + suffix

def padding(string, blockSize):
	if len(string)%blockSize == 0:
		return string + '\x16'*16
	byte = blockSize-(len(string)%blockSize)
	pad = b"".join( bytes.fromhex( hex(byte)[2:].rjust(2,"0") ) for _ in range(byte))
	return string + pad

def cbcEncrypt(plaintext, key, iv):
	plaintext = padding(plaintext, BLOCKSIZE)
	aes = AES.new(key, AES.MODE_CBC, iv)
	ciphertext = aes.encrypt(plaintext)
	return ciphertext

def cbcDecrypt(ciphertext, key, iv):
	aes = AES.new(key, AES.MODE_CBC, iv)
	plaintext = aes.decrypt(ciphertext)
	if b";admin=true;" in plaintext:
		return True
	return False

def main():

	prefix = b"comment1=cooking%20MCs;userdata="
	suffix = b";comment2=%20like%20a%20pound%20of%20bacon"

	plaintext = b"%admin%true"
	plaintext = append(plaintext, prefix, suffix)
	plaintext = padding(plaintext, BLOCKSIZE)

	key = urandom(BLOCKSIZE)
	iv = urandom(BLOCKSIZE)

	ciphertext = cbcEncrypt(plaintext, key, iv)
	semicolon = ciphertext[len(prefix)-BLOCKSIZE] ^ ord(";") ^ ord("%")
	equals = ciphertext[len(prefix)+len(";admin")-BLOCKSIZE] ^ ord("=") ^ ord("%")

	semicolonStart = len(prefix)-BLOCKSIZE
	equalsStart = len(prefix)+len("admin")-BLOCKSIZE

	ciphertext = ciphertext[:len(prefix) - 16] + bytes([semicolon]) + ciphertext[len(prefix)-15:len(prefix) - 10] + bytes([equals]) + ciphertext[len(prefix) - 9:]

	print (cbcDecrypt(ciphertext, key, iv))

if __name__ == "__main__":
	main()
