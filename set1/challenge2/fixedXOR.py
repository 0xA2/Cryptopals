def fixedXOR():
	str0 = raw_input("First hex value > ")
	str1 = raw_input("Second hex value > ")

	if len(str(str0)) != len(str(str1)):
		return "Invalid hex values, both must have the same length"

	dec0 = str0.decode("hex")
	dec1 = str1.decode("hex")
	ret = "".join(chr(ord(dec0[i])^ord(dec1[i])) for i in range(0,len(dec0)))
	print ret.encode("hex")

try:
	fixedXOR()
except TypeError:
	print "Error, odd-length string"
