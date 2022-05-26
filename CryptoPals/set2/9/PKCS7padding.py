import sys

def padding(string, blockSize):
	if len(string)%blockSize == 0:
		return string + b'\x16'*16
	byte = blockSize-(len(string)%blockSize)
	pad = b"".join( bytes.fromhex( hex(byte)[2:].rjust(2,"0") ) for _ in range(byte))
	return string + pad

def main():
	if len(sys.argv) != 3:
		print ("Usage: $ python PKCS7padding.py [STRING] [BLOCKSIZE]")
		sys.exit(1)
	print ( padding(sys.argv[1].encode(), int(sys.argv[2])) )

if __name__ == "__main__":
	main()
