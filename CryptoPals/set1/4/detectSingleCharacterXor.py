
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

def singleByteXor(string, n):
	assert 0 <= n < 256
	ret = b"".join( bytes.fromhex(hex(n^c)[2:].rjust(2,"0")) for c in string)
	return ret

def score(s):
	score = 0
	for c in s:
		cur = chr(c).upper()
		if cur in freqs:
			score += freqs[cur]
	return score

def main():
	with open("4.txt", "r") as file:
		maxScore = 0
		bestString = b""
		line = 0
		lines = file.read().split("\n")
		for i in range(0, len(lines)):
			for j in range(0,256):
				curTry = singleByteXor(bytes.fromhex(lines[i]), j)
				curScore = score(curTry)
				if curScore > maxScore:
					maxScore = curScore
					bestString = curTry
					line = i
		print ("String closest to english: " + bestString.decode() + "\nWith a score of: " + str(maxScore) + "\nIn line: " + str(line))

if __name__ == "__main__":
	main()
