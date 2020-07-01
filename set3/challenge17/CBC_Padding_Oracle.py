from Crypto.Cipher import AES
from os import urandom
from random import randint

import base64

BLOCK_SIZE = 16
KEY_SIZE = 16
IV_SIZE = 16


ciphertexts = ["MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=","MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=","MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==","MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==","MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl","MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==","MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==","MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=","MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=","MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]

def PKCS7_padding_validation(pt):
	if chr(pt[len(pt)-1]).encode()*(pt[len(pt)-1]) == pt[-pt[len(pt)-1]:]:
			return True
	return False

def PKCS7_padding(s):
	if len(s)%BLOCK_SIZE != 0:
		return s + chr((BLOCK_SIZE*(len(s)//BLOCK_SIZE + 1))-len(s)).encode()*((BLOCK_SIZE*(len(s)//BLOCK_SIZE + 1))-len(s))
	return s

def cbc_encrypt(pt,key,iv):
	pt = PKCS7_padding(pt)
	aes = AES.new(key, AES.MODE_CBC, iv)
	ct = aes.encrypt(pt)
	return ct

def cbc_decrypt(ct,key,iv):
	aes = AES.new(key, AES.MODE_CBC, iv)
	pt = aes.decrypt(ct)
	return PKCS7_padding_validation(pt)

def debug_decrypt(ct,key,iv):
	aes = AES.new(key, AES.MODE_CBC, iv)
	pt = aes.decrypt(ct)
	return pt

def getOriginalPadding(lastBlock, key, secondToLastBlock):
	corruptedBlock = secondToLastBlock.copy()
	ret = 0
	while cbc_decrypt(bytes(lastBlock),key,bytes(corruptedBlock)):
		corruptedBlock[ret+1] = 255
		ret += 1
	if ret == 0:
		return []
	return list(chr(BLOCK_SIZE-(ret)).encode() * (BLOCK_SIZE-ret))


def cbc_padding_oracle(ct,key,iv):
	pt = b""

	# To decrypt the first block we'll need to mess with the iv
	ct_blocks = [list(iv)] + [list(ct[i:i + BLOCK_SIZE]) for i in range(0,len(ct),BLOCK_SIZE)]

	# We can use the oracle to retrieve the padding applied to the last plaintext block
	padding = getOriginalPadding(ct_blocks[-1],key,ct_blocks[-2])

	for i in range(0,len(ct_blocks)-1):
		blockToDecrypt = ct_blocks[i+1].copy()
		blockToCorrupt = ct_blocks[i].copy()

		# Since the last block will likely return valid padding regardless if we tamper with the ciphertext we'll handle it seperatly

		# First case - first blocks
		if i != len(ct_blocks) - 2 :
			pt_block = []
			pad = 0

		# Second case - last block
		# We'll use the padding we retrieved earlier
		else:
			pt_block = padding
			pad = len(padding)

		for j in range(BLOCK_SIZE-1-pad,-1,-1):
			if len(pt_block) == 0:
				corruptedBlock = blockToCorrupt.copy()
			else:
				byteToPad = BLOCK_SIZE - 1
				for c in range(0,len(pt_block)):
					corruptedBlock[byteToPad] = (len(pt_block)+1)^pt_block[c]^blockToCorrupt[byteToPad]
					byteToPad -= 1

			for k in range(0,256):
				corruptedBlock[j] = k

				if cbc_decrypt(bytes(blockToDecrypt),key,bytes(corruptedBlock)):
					pt_block.append((len(pt_block)+1)^k^blockToCorrupt[-(len(pt_block)+1)])
					break
		pt += bytes(pt_block[::-1])

	return pt

def main():
	key = urandom(KEY_SIZE)
	iv = urandom(IV_SIZE)
	pt = base64.b64decode(ciphertexts[randint(0,9)])
	ct = cbc_encrypt(pt,key,iv)
	print(cbc_padding_oracle(ct,key,iv))

if __name__ == "__main__":
	main()
