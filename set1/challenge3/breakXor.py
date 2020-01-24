import binascii
import string

freqs = {
    'A': 0.0651738,
    'B': 0.0124248,
    'C': 0.0217339,
    'D': 0.0349835,
    'E': 0.1041442,
    'F': 0.0197881,
    'G': 0.0158610,
    'H': 0.0492888,
    'I': 0.0558094,
    'J': 0.0009033,
    'K': 0.0050529,
    'L': 0.0331490,
    'M': 0.0202124,
    'N': 0.0564513,
    'O': 0.0596302,
    'P': 0.0137645,
    'Q': 0.0008606,
    'R': 0.0497563,
    'S': 0.0515760,
    'T': 0.0729357,
    'U': 0.0225134,
    'V': 0.0082903,
    'W': 0.0171272,
    'X': 0.0013692,
    'Y': 0.0145984,
    'Z': 0.0007836,
    ' ': 0.1918182 
}

valid = string.printable[10:-38] + " "

def singlebytexor(s,byte):
	return "".join(chr(s[i]^byte) for i in range(0,len(s)))

def score(s):
	points = 0
	for ch in s:
		if ch in valid:
			points += freqs[ch.upper()]
	return points

def main():
	with open("3.txt","rb") as f:
		ct = binascii.unhexlify(f.read())
		max_score = 0
		for i in range(0,256):
			cur_try = singlebytexor(ct,i)
			cur_score = score(cur_try)
			if cur_score > max_score:
				max_score = cur_score
				pt = singlebytexor(ct,i)
	print(pt)

if __name__ == "__main__":
	main()
