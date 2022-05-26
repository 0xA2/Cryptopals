import base64

freqs = {
      'A': 0.0651738,
      'B': 0.0124248,
      'C': 0.0217339,
      'D': 0.0349835,
      'E': 0.1241442,
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


def hamming(s1, s2):
	return len( bin( int(bytes.hex(s1),16) ^ int(bytes.hex(s2),16) )[2:].replace("0", "")  )

def getKeySize(ciphertext, maxSize, maxKeys):
	assert (maxSize - 2) > maxKeys
	sizes = {}
	for i in range(2, maxSize):
		chunk1 = hamming(ciphertext[0:i], ciphertext[i:i+i])
		chunk2 = hamming(ciphertext[i:i+i], ciphertext[i+i:i*3])
		chunk3 = hamming(ciphertext[i+i:i*3], ciphertext[i*3:i*4])
		cur = ((chunk1 + chunk2 + chunk3)/3)/i
		sizes[i] = cur
	keys = sorted(sizes.values())[0:maxKeys]
	return [k for k in sizes if sizes[k] in keys]

def getBlocks(ciphertext, keySize):
	blocks = []
	for _ in range(0, keySize):
		blocks.append([])
	for i in range(0,len(ciphertext)):
		blocks[i%keySize].append(ciphertext[i])
	return blocks

def singleByteXor(string, n):
	return b"".join( bytes.fromhex(hex(n^c)[2:].rjust(2,"0")) for c in string)

def score(s):
	score = 0
	for c in s:
		cur = chr(c).upper()
		if cur in freqs:
			score += freqs[cur]
	return score

def getKey(blocks):
	key = b""
	for block in blocks:
		maxScore = 0
		keyGuess = b""
		for i in range(0,256):
			curTry = singleByteXor(block,i)
			curScore = score(curTry)
			if curScore > maxScore:
				maxScore = curScore
				keyGuess = bytes([i])
		key += keyGuess
	return key

def keyXor(string, key):
	ret = b"".join( bytes.fromhex(hex(string[i]^key[i%len(key)])[2:].rjust(2,"0")) for i in range(0,len(string)))
	return ret

def main():
	with open("6.txt", "r") as file:
		ciphertext = base64.b64decode( "".join(line[:-1] for line in file) )
		keySizes = getKeySize(ciphertext, 50, 5)
		plaintext = b""
		key = b""
		maxScore = 0
		for size in keySizes:
			blocks = getBlocks(ciphertext, size)
			possibleKey = getKey(blocks)
			possiblePlaintext = keyXor(ciphertext, possibleKey)
			curScore = score(possiblePlaintext)
			if curScore > maxScore:
				maxScore = curScore
				plaintext = possiblePlaintext
				key = possibleKey
		print ("Plaintext:\n" + plaintext.decode())
		print ("Key:\n" + key.decode())

if __name__ == "__main__":
	main()
