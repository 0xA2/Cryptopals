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

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
valid_letters = letters + letters.lower() + " " 

def genblock(s,keysize,iter):
	block = ""
	for i in range(0,len(s)/keysize):
		block += s[(i*keysize)+iter]
	return block

def score(s):
	score = 0
	for i in s:
		if i in valid_letters:
			c = i.upper()
			score += freqs[c]
	return score

def singlebyteXOR(s):
	ret = "".join(chr(ord(s[j])^0) for j in range(0,len(s)))
	max_score = score(ret)
	for i in range(1,256):
		curr = "".join(chr(ord(s[j])^i) for j in range(0,len(s)))
		curr_score = score(curr)
		if curr_score > max_score:
			max_score = curr_score
			ret = curr
			iter = i
	return chr(iter)

def hamming(s1,s2):
	bin1 = bin(int(s1.encode("hex"),16))[2:]
	bin2 = bin(int(s2.encode("hex"),16))[2:]
	if len(bin1) != len(bin2):
		if len(bin1) < len(bin2):
			bin1 = bin1.rjust(len(bin2), "0")
		else:
			bin2 = bin2.rjust(len(bin1),"0")
	distance = 0
	for i in range(0,len(bin2)):
		if bin1[i] != bin2[i]:
			distance += 1
	return float(distance)

def breakrepeatingXOR(s):
	dict = {}
	for keysize in range(2,42):
		block1 = "".join(s[i] for i in range(0,keysize))
		block2 = "".join(s[i] for i in range(keysize, keysize*2))
		block3 = "".join(s[i] for i in range(keysize*2,keysize*3))
		block4 = "".join(s[i] for i in range(keysize*3,keysize*4))
		dist = (hamming(block1,block2) + hamming(block2,block3) + hamming(block3,block4)) / 3.
		normalized_edit_dist = dist/float(keysize)
		dict.update({keysize :normalized_edit_dist})
	potential_keys = sorted(list(dict.values()))[0:3]
	best_score = 0
	for i in range(0,len(potential_keys)):
		key = ""
		keysize = dict.keys()[dict.values().index(potential_keys[i])]
		for i in range(0,keysize):
			block = genblock(s,keysize,i)
			key += singlebyteXOR(block)
		curr_score = score(decript(s,key))
		if curr_score > best_score:
			real_key = key
	print decript(s,real_key)

def decript(s, key):
	full_key = key
	while len(full_key) < len(s):
		full_key += key
	ret = "".join(chr(ord(s[i])^ord(full_key[i])) for i in range(0,len(s)))
	return ret

def main():
	with open("6.txt","r") as file:
		text = ""
		for line in file:
			text += line[:-1]
	s = text.decode("base64")
	breakrepeatingXOR(s)
main()
