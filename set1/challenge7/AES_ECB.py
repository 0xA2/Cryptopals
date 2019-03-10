from Crypto.Cipher import AES

def main():
	with open("7.txt", "r") as file:
		s = "".join(line[:-1] for line in file)
	passphrase = "YELLOW SUBMARINE"
	aes = AES.new(passphrase, AES.MODE_ECB)
	print aes.decrypt(s.decode("base64"))
main()
