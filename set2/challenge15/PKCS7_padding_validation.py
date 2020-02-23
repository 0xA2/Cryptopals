
BLOCK_SIZE = 16

def PKCS7_padding_validation(pt):
	if len(pt)%BLOCK_SIZE == 0 and pt[len(pt)-1] >= BLOCK_SIZE:
		return b"Valid padding > " + pt
	elif chr(pt[len(pt)-1]).encode()*(pt[len(pt)-1]) == pt[-pt[len(pt)-1]:] and pt[len(pt)-1] < BLOCK_SIZE:
		return b"Valid padding, plaintext > " + strip_padding(pt)
	else:
		return "Invalid padding!"

def strip_padding(pt):
	return pt[:-pt[len(pt)-1]]

def main():
	pt = b"YELLOW SUBMARINE" 
	print (PKCS7_padding_validation(pt))

if __name__ == "__main__":
	main()
