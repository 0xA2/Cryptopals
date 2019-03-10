def encript(s, key):
	full_key = key
	while len(full_key) < len(s):
		full_key += key
	ret = "".join(chr(ord(s[i])^ord(full_key[i])) for i in range(0,len(s)))
	print ret.encode("hex")

def main():
	s = raw_input("String to encode > ")
	k = raw_input("Key for encoding > ")
	encript(s,k)
main()
