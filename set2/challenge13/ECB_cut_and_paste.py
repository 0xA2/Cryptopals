from Crypto.Cipher import AES
from os import urandom

import base64
import random
import re
import sys

BLOCK_SIZE =16
KEY_SIZE = 16

key = urandom(KEY_SIZE)

def PKCS7_padding(s):
	if len(s)%BLOCK_SIZE != 0:
		return s + chr((BLOCK_SIZE*(len(s)//BLOCK_SIZE)+BLOCK_SIZE)-len(s))*((BLOCK_SIZE*(len(s)//BLOCK_SIZE + 1))-len(s))
	return s

def enc(pt):
	pt = PKCS7_padding(pt)
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
	if re.match(".[&=].",email):
		return "Invalid characters"
	profile = {
		'email':email,
		'uid':1337,
		'role':'user',
	}
	ret = "email={}&uid={}&role={}".format(profile["email"],profile["uid"],profile["role"])
	return ret

def ECB_cut_and_paste(profile,newrole):
	return  dec(enc(profile)[:32] + enc("admin"))[:-11]

def main():
	email = "42@mail.com"
	#Since len(email) = 11 the second block of enc(profile(email)) will end in "role="
	#To create a valid admin profile we'll take the first 2 blocks of enc(profile(email)) and concat enc("admin")
	#The decrypted result will be a valid admin profile
	#block1			 	block2          	block3
	#email=42@mail.co	m&uid=1337&role= 	admin(padding)
	admin_profile =  parser(ECB_cut_and_paste(profile(email),"admin"))
	print ("Registered the email > {}\nCorrespondent uid > {}\nRespective role > {}".format(admin_profile["email"],admin_profile["uid"],admin_profile["role"]))

if __name__ == '__main__':
	main()

