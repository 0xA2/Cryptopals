from Crypto.Cipher import AES
from os import urandom

BLOCK_SIZE = 16
KEY_SIZE = 16
IV_SIZE = 16

key = urandom(KEY_SIZE)
iv = urandom(IV_SIZE)

prefix = b"comment1=cooking%20MCs;userdata="
suffix = b";comment2=%20like%20a%20pound%20of%20bacon" 

def filter_and_pad(pt):
	pt = pt.replace(b";",b"%").replace(b"=",b"%")
	return prefix + pt + suffix

def PKCS7_padding(s):
	if len(s)%BLOCK_SIZE != 0:
		return s + chr((BLOCK_SIZE*(len(s)//BLOCK_SIZE)+BLOCK_SIZE)-len(s)).encode()*((BLOCK_SIZE*(len(s)//BLOCK_SIZE + 1))-len(s))
	return s

def encrypt(pt):
	pt = PKCS7_padding(pt)
	aes = AES.new(key, AES.MODE_CBC, iv)
	ct = aes.encrypt(pt)
	return ct

def cbc_decrypt(ct):
	aes = AES.new(key, AES.MODE_CBC, iv)
	dec = aes.decrypt(ct)
	if b";admin=true;" in dec:
		return True
	return False

def CBC_bitflipping_attack(ct):
	semicolon = ct[len(prefix)-16] ^ ord("%") ^ ord(";")
	equals = ct[len(prefix)-10] ^ ord("%") ^ ord("=")
	return ct[:len(prefix) - 16] + bytes([semicolon]) + ct[len(prefix)-15:len(prefix) - 10] + bytes([equals]) + ct[len(prefix) - 9:]

def main():
	pt = b";admin=true"
	ct = encrypt(filter_and_pad(pt))
	alt_ct = (CBC_bitflipping_attack(ct))
	print (cbc_decrypt(alt_ct))

if __name__ == "__main__":
	main()
