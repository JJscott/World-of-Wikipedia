#!/bin/env python

from __future__ import division
import math, random, sys


def main():
	count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
	for i in xrange(count):
		# this is not a completely even spherical distribution
		x = random.random() * 2.0 - 1
		y = random.random() * 2.0 - 1
		z = random.random() * 2.0 - 1
		m = math.sqrt(x**2 + y**2 + z**2)
		x /= m
		y /= m
		z /= m
		long = math.atan2(x, z)
		lat = math.atan(y / math.sqrt(x**2 + z**2))
		year = 1900.0 + random.random() * 115.0
		print '{0}\t{1}\t{2}'.format(math.degrees(long), math.degrees(lat), year)
	# }
# }

if __name__ == '__main__':
	main()
# }