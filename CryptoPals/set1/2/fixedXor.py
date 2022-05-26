import sys

def xor(s1, s2):
	assert len(s1) == len(s2)
	ret = b"".join( bytes.fromhex(hex(s1[i]^s2[i])[2:].rjust(2,"0")) for i in range(0,len(s1)) )
	return ret

def main():
	if len(sys.argv) != 3  or ( len(sys.argv[1]) != len(sys.argv[2]) ):
		print ("Usage: $ python fixedXor.py [FIRST_HEX_STRING] [SECOND_HEX_STRING]\nNote: Strings must have the same length")
		sys.exit(1)
	try:
		print ( xor(bytes.fromhex(sys.argv[1]), bytes.fromhex(sys.argv[2])).decode() )
	except:
		print ("Usage: $ python fixedXor.py [FIRST_HEX_STRING] [SECOND_HEX_STRING]\nStrings must have the same length")
if __name__ == "__main__":
	main()
