import sys

def keyXor(string, key):
	ret = b"".join( bytes.fromhex(hex(string[i]^key[i%len(key)])[2:].rjust(2,"0")) for i in range(0,len(string)))
	return ret

def main():
	if len(sys.argv) != 3:
		print ("Usage: $ python repeatingKeyXor.py [ASCII_STRING] [KEY]")
		sys.exit(1)
	try:
		ct = keyXor(sys.argv[1].encode(), sys.argv[2].encode())
		print (bytes.hex(ct))
	except:
		print ("Usage: $ python repeatingKeyXor.py [ASCII_STRING] [KEY]")

if __name__ == "__main__":
	main()
