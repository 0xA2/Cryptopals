
BLOCKSIZE = 16

def scoreECB(ciphertext):
	blocks = [ciphertext[i:i+BLOCKSIZE*2] for i in range(0, len(ciphertext), BLOCKSIZE*2)]
	score = len(blocks) - len(set(blocks))
	return score

def main():
	with open("8.txt", "r") as file:
		ciphertext = [line[:-1] for line in file]
		maxScore = 0
		line = 0
		for i in range(0, len(ciphertext)):
			curScore = scoreECB(ciphertext[i])
			if curScore > maxScore:
				maxScore = curScore
				line = i
		print ("Found potential AES ECB encrypted string at line: " + str(line) + "\nWith a score of: " + str(maxScore))

if __name__ == "__main__":
	main()
