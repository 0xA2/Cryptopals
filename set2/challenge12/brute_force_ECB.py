from Crypto.Cipher import AES
import string
from os import urandom

KEY_SIZE = 16
IV_SIZE = 16
BLOCK_SIZE = 16
HOW_MANY_BLOCKS = 9
BLOCKS = HOW_MANY_BLOCKS * BLOCK_SIZE

key = urandom(KEY_SIZE)

flag = '''Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK'''.decode("base64")


def PKCS7_padding(pt):
	if len(pt)%16 == 0 and len(pt) != 0:
		return pt
	else:
		return pt.ljust(16*(len(pt)/16)+16,chr((16*(len(pt)/16)+16)-len(pt)))

def enc(pt):
	pt = PKCS7_padding(pt)
	aes = AES.new(key, AES.MODE_ECB)
	ct = aes.encrypt(pt)
	return ct


def main():
	p = string.printable
	known_bytes = ""
	for i in range(0,BLOCKS):
		for b in p:
			if enc('A'*(BLOCKS - 1  - i) + known_bytes + b)[:(BLOCKS-1)] == enc(b'A'*(BLOCKS - 1  - i) + flag)[:(BLOCKS -1 )]:
				known_bytes += b
				break
	print known_bytes

if __name__ == '__main__':
	main()
