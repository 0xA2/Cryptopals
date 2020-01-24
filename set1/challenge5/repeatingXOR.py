import binascii

def keyxor(s, key):
	return binascii.hexlify("".join([chr(s[i]^key[i%len(key)]) for i in range(max(len(s),len(key)))]).encode())

def main():
	print(keyxor(b'Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal',b'ICE'))

if __name__ == "__main__":
	main()
