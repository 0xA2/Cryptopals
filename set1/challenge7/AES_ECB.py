from Crypto.Cipher import AES
import base64

def main():
	with open("7.txt", "r") as file:
		s = "".join(line[:-1] for line in file)
	passphrase = "YELLOW SUBMARINE"
	aes = AES.new(passphrase, AES.MODE_ECB)
	print (aes.decrypt(base64.b64decode(s)))

if __name__ == "__main__":
	main()

