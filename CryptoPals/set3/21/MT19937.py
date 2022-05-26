import sys

# Coefficients for MT19937-32
w, n, m, r = 32, 624, 397, 31
a = 0x9908b0df
u, d = 11, 0xffffffff
s, b = 7, 0x9d2c5680
t, c = 15, 0xefc60000
l = 18
f = 1812433253

MT = [0]*n
index = n+1
lowerMask = (1 << r) - 1
upperMask = 0x80000000 # lowest w bits of (not lower_mask)

def seedMT(seed):
	#index = n
	MT[0] = seed
	for i in range(1, n):
		MT[i] = (f * (MT[i-1] ^ (MT[i-1] >> (w-2)) ) + i ) & 0xffffffff


def twist():
	for i in range(n):
		x = (MT[i] & upperMask) + (MT[(i+1)%n] & lowerMask)
		xA = x >> 1
		if (x%2) != 0:
			xA = xA ^ a
		MT[i] = MT[(i+m)%n] ^ xA

def extractNumber():
	global index
	if index >= n:
		twist()
		index = 0

	y = MT[index]
	y = y ^ ( (y >> u) & d )
	y = y ^ ( (y << s) & b )
	y = y ^ ( (y << t) & c )
	y = y ^ ( y >> l )
	index += 1
	return y & 0xffffffff

def main():

	seedMT(0)
	print ( extractNumber() )

if __name__ == "__main__":
	main()
