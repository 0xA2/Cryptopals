from Crypto.Cipher import AES
from os import urandom

import base64

BLOCKSIZE = 16

plaintexts = ['SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==', 'Q29taW5nIHdpdGggdml2aWQgZmFjZXM=', 'RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==', 'RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=', 'SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk', 'T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==', 'T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=', 'UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==', 'QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=', 'T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl', 'VG8gcGxlYXNlIGEgY29tcGFuaW9u', 'QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==', 'QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=', 'QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==', 'QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=', 'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=', 'VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==', 'SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==', 'SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==', 'VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==', 'V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==', 'V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==', 'U2hlIHJvZGUgdG8gaGFycmllcnM/', 'VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=', 'QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=', 'VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=', 'V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=', 'SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==', 'U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==', 'U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=', 'VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==', 'QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu', 'SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=', 'VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs', 'WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=', 'SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0', 'SW4gdGhlIGNhc3VhbCBjb21lZHk7', 'SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=', 'VHJhbnNmb3JtZWQgdXR0ZXJseTo=', 'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=']

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

def score(s):
	score = 0
	for c in s:
		cur = chr(c).upper()
		if cur in freqs:
			score += freqs[cur]
	return score

def singleByteXor(string, n):
	return b"".join( bytes.fromhex(hex(n^c)[2:].rjust(2,"0")) for c in string)

def xorStrings(data0, data1):
	ret = b"".join(bytes.fromhex(hex(data0[i]^data1[i])[2:].rjust(2,'0')) for i in range(min(len(data0),len(data1))))
	return ret

def encrypt(plaintext, key, nonce):
	aes = AES.new(key, AES.MODE_ECB)
	counter = 0
	keyStream = b""
	keyLen = (len(plaintext)//BLOCKSIZE) + 1 if len(plaintext)%16 != 0 else (len(plantext)//BLOCKSIZE)
	for i in range(0, keyLen):
		curCounter = bytes.fromhex(hex(counter)[2:(BLOCKSIZE+2)].rjust(BLOCKSIZE,'0'))[::-1]
		keyStream += aes.encrypt(nonce + curCounter)
		counter += 1
	return xorStrings(plaintext, keyStream)

def decrypt(ciphertext, key, nonce):
	aes = AES.new(key, AES.MODE_ECB)
	counter = 0
	keyStream = b""
	keyLen = (len(ciphertext)//BLOCKSIZE) + 1 if len(ciphertext)%16 != 0 else (len(ciphertext)//BLOCKSIZE)
	for i in range(0, keyLen):
		curCounter = bytes.fromhex(hex(counter)[2:(BLOCKSIZE+2)].rjust(BLOCKSIZE,'0'))[::-1]
		keyStream += aes.encrypt(nonce + curCounter)
		counter += 1
	return xorStrings(ciphertext, keyStream)

def getBlocks(ciphertexts, keySize):
	ret = []
	for i in range(keySize):
		block = b""
		for j in range(len(ciphertexts)):
			if i < len(ciphertexts[j]):
				block += bytes([ciphertexts[j][i]])
			else:
				continue
		ret.append(block)
	return ret

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

def main():
	key = urandom(BLOCKSIZE)
	nonce = b'\x00'*(BLOCKSIZE//2)
	ciphertexts = []
	for pt in plaintexts:
		ciphertexts.append(decrypt(base64.b64decode(pt),key,nonce))
	keySize = len(max(ciphertexts, key=len))
	blocks = getBlocks(ciphertexts, keySize)
	keyGuess = getKey(blocks)
	for i in range(len(ciphertexts)):
		print (xorStrings(ciphertexts[i],keyGuess))

if __name__ == "__main__":
	main()
