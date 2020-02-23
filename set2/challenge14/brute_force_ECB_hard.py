from Crypto.Cipher import AES
from os import urandom
from random import randint

import base64
import string

KEY_SIZE = 16
IV_SIZE = 16
BLOCK_SIZE = 16
HOW_MANY_BLOCKS = 9
PT_LEN = HOW_MANY_BLOCKS * BLOCK_SIZE

def PKCS7_padding(s):
	if len(s)%BLOCK_SIZE != 0:
		return s + chr((BLOCK_SIZE*(len(s)//BLOCK_SIZE)+BLOCK_SIZE)-len(s)).encode()*((BLOCK_SIZE*(len(s)//BLOCK_SIZE + 1))-len(s))
	return s

def enc(pt,key):
	pt = PKCS7_padding(pt)
	aes = AES.new(key, AES.MODE_ECB)
	ct = aes.encrypt(pt)
	return ct

def brute_force_ECB(pt,key):
	known_bytes = b""
	flag = enc(b"STIMULUSRESPONSE",key)
	for i in range(0,PT_LEN):
		cur_try = b""
		while True:
			cur_try = enc(urandom(randint(0,255)) + b"STIMULUSRESPONSE" + b"A"*(PT_LEN - 1 - i) + pt,key)
			if flag in cur_try:
				break
		for byte in string.printable.encode():
			while True:
				cur_byte = enc(urandom(randint(0,255)) + b"STIMULUSRESPONSE" + b"A"*(PT_LEN-1-i) + known_bytes  + chr(byte).encode(),key)
				if flag in cur_byte:
					break
			if cur_byte.split(flag)[1][:PT_LEN - 1] == cur_try.split(flag)[1][:PT_LEN - 1]:
				known_bytes += chr(byte).encode()
				break

	return known_bytes.decode()

def main():
	pt = base64.b64decode('''Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK''')
	key = urandom(KEY_SIZE)
	print (brute_force_ECB(pt,key))

if __name__ == '__main__':
	main()
