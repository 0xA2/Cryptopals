import base64
import sys

def main():
	if len(sys.argv) != 2:
		print ("Usage: $ python hex2base64.py [HEX_STRING]")
		sys.exit(1)
	try:
		print ( base64.b64encode(bytes.fromhex(sys.argv[1])) )
	except:
		print ("Usage: $ python hex2base64.py [HEX_STRING]")
if __name__ == "__main__":
	main()

