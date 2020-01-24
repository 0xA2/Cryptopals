import binascii
import base64
import string

MAXSIZE = 42

TOP_SCORING_KEYSIZE_BOUND = 5

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

valid = string.printable[10:-38] + " "

def singlebytexor(s,byte):
	return "".join(chr(s[i]^byte) for i in range(0,len(s)))

def score(s):
	points = 0
	for ch in s:
		if ch in valid:
			points += freqs[ch.upper()]
	return points

def hamming(s1,s2):
	return len(bin(int(binascii.hexlify(s1),16)^int(binascii.hexlify(s2),16))[2:].replace("0",""))

def getKeySize(ct):
	assert MAXSIZE < len(ct)//4
	dict = {}
	for i in range(2,MAXSIZE):
		dict[i] = ((hamming(ct[:i],ct[i:-(len(ct)-2*i)]) + hamming(ct[i:-(len(ct)-i*2)],ct[i*2:-(len(ct)-i*3)]) + hamming(ct[i*2:-(len(ct)-i*3)],ct[i*3:-(len(ct)-i*4)]))/3)/i
	values = sorted(dict.values())[0:TOP_SCORING_KEYSIZE_BOUND]
	return [key for key in dict if dict[key] in values]

def getBlocks(ct,key_size):
	ret=[]
	for i in range(0,len(key_size)):
		temp = []
		for j in range(0,key_size[i]):
			parts = b""
			for k in range(j,len(ct),key_size[i]):
				parts += bytes([ct[k]])
			temp.append(parts)
		ret.append(temp)
	return ret

def getkey(ct_blocks):
	potential_keys = []
	for blocks in ct_blocks:
		key = ""
		for single_block in blocks:
			max_score = 0
			key_part = ""
			for i in range(0,256):
				cur_try = singlebytexor(single_block,i)
				cur_score = score(cur_try)
				if cur_score > max_score:
					max_score = cur_score
					key_part = chr(i)
			key += key_part
		potential_keys.append(key)
	return potential_keys

def breakReXor(ct,potential_keys):
	max_score = 0
	pt = ""
	for key in potential_keys:
		potential_pt = "".join(chr(ct[i]^ord(key[i%len(key)])) for i in range(0,len(ct)))
		cur_score = score(potential_pt)
		if cur_score > max_score:
			max_score = cur_score
			pt = potential_pt
	return pt

def main():
	with open("6.txt","r") as f:
		ct = base64.b64decode("".join(line[:-1] for line in f))
		key_size = getKeySize(ct)
		blocks = getBlocks(ct,key_size)
		possible_keys = getkey(blocks)
		pt = breakReXor(ct,possible_keys)
		print (pt)
if __name__ == "__main__":
	main()

