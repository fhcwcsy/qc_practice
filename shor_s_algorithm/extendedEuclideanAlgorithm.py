# copied from https://www.techiedelight.com/extended-euclidean-algorithm-implementation/ 
def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		gcd, x, y = egcd(b % a, a)
		return (gcd, y - (b//a) * x, x)

