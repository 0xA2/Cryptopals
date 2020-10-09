import base64
import binascii
import os

from Crypto.Cipher import AES
from Crypto.Util import Counter

def encrypt(pt,key):
	iv = os.urandom(16)
	ctr = Counter.new(128, initial_value = int(binascii.hexlify(iv),16), little_endian = True)
	aes = AES.new(key, AES.MODE_CTR, counter = ctr)
	ct = aes.encrypt(pt)
	return (ct,iv)

def decrypt(ct,key):
	iv = ct[1]
	ctr = Counter.new(128, initial_value = int(binascii.hexlify(iv),16), little_endian = True)
	aes = AES.new(key, AES.MODE_CTR, counter=ctr)
	return aes.decrypt(ct[0])

def main():
	pt = b"Secret"
	key = b'YELLOW SUBMARINE'
	ct = encrypt(pt,key)
	print (decrypt(ct,key))

if __name__ == "__main__":
	main()
