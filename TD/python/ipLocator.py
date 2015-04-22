import sys
import re
import csv
from bisect import bisect_right

_ipv4_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
_ipv6_pattern = r'^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$'


class IPGeolocator(object):
	"""docstring for ClassName"""
	def __init__(self, ipv4_db, ipv6_db):
		self._ipv4_ip_int = []
		self._ipv4_ip_mask = []
		self._ipv4_long_lat = []

		self._ipv6_ip_int = []
		self._ipv6_ip_mask = []
		self._ipv6_long_lat = []

		self._init(ipv4_db, ipv6_db)


	def _init(self, ipv4_db, ipv6_db):
		if ipv4_db:
			# print 'Loading ipv4-geolocation data ...'
			self._load_ipv4_database(ipv4_db)
		if ipv6_db:
			# print 'Loading ipv6-geolocation data ...'
			self._load_ipv6_database(ipv6_db)
		# print 'Done'


	def _load_ipv4_database(self, filepath):
		with open(filepath, 'rb') as csvfile:		# safely open file
			ipreader = csv.reader(csvfile)			# open file as CSV reader
			for line in ipreader:	 				# ignore the first line (names)

				if line[-2] and line[-1]: 			# if longtitude and latitude exist

					ip_str, mask_str = line[0].split('/')			# retrieve ip and mask as a string
					mask = ipv4_mask(int(mask_str))					# create bit mask
					ip = int_from_ipv4(ip_str) & mask				# bitwise-and the ip with mask (just in case)
					long_lat = (float(line[-2]), float(line[-1]))	# compile a longitude-latitude pair

					self._ipv4_ip_int.append(ip)
					self._ipv4_ip_mask.append(mask)
					self._ipv4_long_lat.append(long_lat)


	def _load_ipv6_database(self, filepath):
		with open(filepath, 'rb') as csvfile:		# safely open file
			ipreader = csv.reader(csvfile)			# open file as CSV reader
			for line in ipreader: 					# ignore the first line (names)

				if line[-2] and line[-1]: 			# if longtitude and latitude exist

					ip_str, mask_str = line[0].split('/')			# retrieve ip and mask as a string
					mask = ipv6_mask(int(mask_str))					# create bit mask
					ip = int_from_ipv6(ip_str) & mask				# bitwise-and the ip with mask (just in case)
					long_lat = (float(line[-2]), float(line[-1]))	# compile a longitude-latitude pair

					self._ipv6_ip_int.append(ip)
					self._ipv6_ip_mask.append(mask)
					self._ipv6_long_lat.append(long_lat)

	# Returns a long/lat pair, or None if cannot match
	def locate_ip(self, addr):
		#determine wether ipv4/v6
		if bool(re.match(_ipv4_pattern, addr)):
			return _bin_search_ip(int_from_ipv4(addr), self._ipv4_ip_int, self._ipv4_ip_mask, self._ipv4_long_lat)

		elif bool(re.match(_ipv6_pattern, addr)):
			return _bin_search_ip(int_from_ipv6(addr), self._ipv6_ip_int, self._ipv6_ip_mask, self._ipv6_long_lat)

		# print 'Error: IP string not recognised as either IPv4 or IPv6'
		return None


def _bin_search_ip(addr, ip_list, mask_list, long_lat_list):
	i = bisect_right(ip_list, addr)
	if i and ip_list[i-1] == addr & mask_list[i-1]:
		return long_lat_list[i-1]
	return None

def int_from_ipv4(addr):
	return reduce(lambda a,b: a<<8 | b, map(int, addr.split(".")))

def ipv4_mask(bitnum):
	return ~(~(0) << bitnum) << (32 - bitnum)

def int_from_ipv6(addr):
	addr = addr.replace('::', ':' + '0:' * (8 - sum(map(lambda x: len(filter(None, x.split(':'))), addr.split('::')))))
	return reduce(lambda a,b: a<<16 | b, map(lambda x: int(x, 16), filter(None, addr.split(":"))))

def ipv6_mask(bitnum):
	return ~(~(0) << bitnum) << (128 - bitnum)














