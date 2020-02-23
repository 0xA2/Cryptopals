import binascii

BLOCK_SIZE = 16

def PKCS7_padding(s):
	if len(s)%BLOCK_SIZE != 0:
		return s + chr((BLOCK_SIZE*(len(s)//BLOCK_SIZE)+BLOCK_SIZE)-len(s)).encode()*((BLOCK_SIZE*(len(s)//BLOCK_SIZE + 1))-len(s))
	return s

def main():
	pt = b"YELLOW SUBMARINE"
	print (PKCS7_padding(pt))

if __name__ == "__main__":
	main()
