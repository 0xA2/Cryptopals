

def PKCS7paddingValidation(string, blocksize):
	byteNum = string[len(string)-1]
	toVerify = string[-byteNum:]
	if toVerify == chr(byteNum).encode()*byteNum:
		return True
	return False

def main():
	valid = b"ICE ICE BABY\x04\x04\x04\x04"
	invalid = b"ICE ICE BABY\x05\x05\x05\x05"
	print (PKCS7paddingValidation(valid, 16))
	print (PKCS7paddingValidation(invalid, 16))
if __name__ == "__main__":
	main()
