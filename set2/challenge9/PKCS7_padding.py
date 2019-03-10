def main():
	input_bytes = raw_input("Message to pad > ")
	if (len(input_bytes))%16 == 0:
		print "Message length is a multiple of 16, no padding needed"
	else:
		print input_bytes.ljust(16*(len(input_bytes)/16)+16,chr((16*(len(input_bytes)/16)+16)-len(input_bytes))).encode("hex")
main()
