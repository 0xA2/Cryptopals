from Crypto.Cipher import AES
with open("10.txt","r") as file:
	s = "".join(line[:-1] for line in file)
passphrase = "YELLOW SUBMARINE"
iv = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
aes = AES.new(passphrase, AES.MODE_CBC, iv)
print aes.decrypt(s.decode("base64"))

