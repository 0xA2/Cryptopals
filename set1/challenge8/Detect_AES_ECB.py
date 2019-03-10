BLOCK_SIZE = 16
def AES_ECB_Score(line):
	substrings = [line[i:i + BLOCK_SIZE] for i in range(0, len(line), BLOCK_SIZE)]
	score = len(substrings) - len(set(substrings))
	print score
	return score

def main():
	best_score = 0
	with open("8.txt","r") as file:
		count = 0
		for line in file:
			curr_score = AES_ECB_Score(line.strip("\n")) 
			if curr_score > best_score:
				best_score = curr_score
				ret_line = line
				ret_count = count
			count += 1
	print "Line with best score > " + str(ret_line) + "Number > " + str(ret_count) + "\nWith a score of > " + str(best_score)

main()
