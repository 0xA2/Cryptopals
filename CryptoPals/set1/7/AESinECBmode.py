import base64

from Crypto.Cipher import AES

def main():

	with open("7.txt", "r") as file:
		string = "".join(line[:-1] for line in file)
		key = b"YELLOW SUBMARINE"
		aes = AES.new(key, AES.MODE_ECB)
		print (aes.decrypt(base64.b64decode(string)).decode())

if __name__ == "__main__":
	main()
