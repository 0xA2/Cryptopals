import binascii

def fixedXOR(s1,s2):
	if len(s1) != len(s2):
		return "Strings with diferent length!"
	return hex(int(s1,16)^int(s2,16))[2:]

def main():
	print(fixedXOR(b'1c0111001f010100061a024b53535009181c',b'686974207468652062756c6c277320657965'))

if __name__ == "__main__":
	main()
