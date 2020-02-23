from Crypto.Cipher import AES
import base64

def cbc_decrypt(ct,passphrase,iv):
	aes = AES.new(passphrase, AES.MODE_CBC, iv)
	return aes.decrypt(base64.b64decode(ct))

def main():
	with open("10.txt","r") as file:
		s = "".join(line[:-1] for line in file)
	passphrase = "YELLOW SUBMARINE"
	iv = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
	print (cbc_decrypt(s,passphrase,iv))

if __name__ == "__main__":
	main()
