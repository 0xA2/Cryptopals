from Crypto.Cipher import AES

import base64

def main():
	with open("10.txt", "r") as file:
		s = "".join(line[:-1] for line in file)
		passphrase = "YELLOW SUBMARINE"
		iv = b"\x00"*16
		aes = AES.new(passphrase.encode(), AES.MODE_CBC, iv)
		print (aes.decrypt(base64.b64decode(s)).decode())
if __name__ == "__main__":
	main()
