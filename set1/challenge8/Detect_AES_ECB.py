BLOCK_SIZE = 16

def AES_ECB_Score(line):
	blocks = [line[i:i + BLOCK_SIZE*2] for i in range(0, len(line), BLOCK_SIZE*2)]
	score = len(blocks) - len(set(blocks))
	return score

def detect_AES(file_content):
	ret = ["",0]
	for line in file_content:
		cur_score = AES_ECB_Score(line)
		if cur_score > ret[1]:
			ret = [line,cur_score]
	return ret

def main():
	with open("8.txt","r") as file:
		content = [line.strip("\n") for line in file]
		print ("Line encrypted with AES > " + str(detect_AES(content)[0]) + "\nWith a score of > " + str(detect_AES(content)[1]))

if __name__ == "__main__":
	main()


