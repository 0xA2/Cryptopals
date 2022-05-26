from Crypto.Cipher import AES
from os import urandom

import base64
import random
import sys

BLOCKSIZE = 16
KEYSIZE = 16

key = urandom(KEYSIZE)

def PKCS7padding(string, blockSize):
	if len(string)%blockSize == 0:
		return string.encode() + b'\x16'*16
	byte = blockSize-(len(string)%blockSize)
	pad = b"".join( bytes.fromhex( hex(byte)[2:].rjust(2,"0") ) for _ in range(byte))
	return string.encode() + pad

def enc(pt):
	pt = PKCS7padding(pt, BLOCKSIZE)
	aes = AES.new(key, AES.MODE_ECB)
	return aes.encrypt(pt)

def dec(ct):
	aes = AES.new(key, AES.MODE_ECB)
	return aes.decrypt(ct).decode()

def parser(cookie):
	parts = cookie.split("&")
	dict = {}
	for part in parts:
		key_value = part.split("=")
		dict[key_value[0]] = key_value[1]
	return dict

def profile(email):
	if "&" in email or "=" in email:
		print ("Invalid characters")
		sys.exit(1)

	profile = {
		'email':email,
		'uid':1337,
		'role':'user',
	}
	ret = "email={}&uid={}&role={}".format(profile["email"],profile["uid"],profile["role"])
	return ret

def ECBcutAndPaste(profile,newrole):
	return  dec(enc(profile)[:32] + enc(newrole))[:-11]

def main():
	email = "42@mail.com"
	#Since len(email) = 11 the second block of enc(profile(email)) will end in "role="
	#To create a valid admin profile we'll take the first 2 blocks of enc(profile(email)) and concat enc("admin")
	#The decrypted result will be a valid admin profile
	#block1			 	block2          	block3
	#email=42@mail.co	m&uid=1337&role= 	admin(padding)
	adminProfile =  parser(ECBcutAndPaste(profile(email),"admin"))
	print ("Registered the email > {}\nCorrespondent uid > {}\nRespective role > {}".format(adminProfile["email"],adminProfile["uid"],adminProfile["role"]))
	print ("Object > " + str(adminProfile))

if __name__ == '__main__':
	main()
