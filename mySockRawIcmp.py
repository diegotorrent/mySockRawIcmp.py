# DFT 2023-09-07
# mySockRawIcmp.py

import argparse
import socket
import struct
from datetime import datetime
from time import sleep


class SockRawIcmp:

    def __init__(self, interface=b'eth0'):
        # SockRawIcmp Constructor
        self.interval = 5
        self.timeout = 5
        self.interface = interface
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, self.interface)
        self.sock.settimeout(self.timeout)

    def ping(self, dest_ip='0.0.0.0'):
        # ICMP Echo Request Type 8
        try:

            icmp_type = 8
            icmp_code = 0
            icmp_checksum = 0
            icmp_identifier = 12345
            icmp_sequence = 1
            icmp_data = b'icmp_data'

            icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_identifier, icmp_sequence)

            icmp_checksum = socket.htons(
                ~(icmp_type + icmp_code + icmp_checksum + icmp_identifier + icmp_sequence) & 0xFFFF)

            icmp_header = icmp_header[:2] + struct.pack('H', icmp_checksum) + icmp_header[4:]

            packet = icmp_header + icmp_data

            cont = 0

            while True:

                print("\033[2J", "\n" + "*" * 60 + "\nRequest", cont, "\t\t\t", datetime.now())

                print("interface", "Dir.", "Size", "\tAddress ", "\tType")

                print(i.decode("utf-8"), "->", len(packet), "\t\tIP: ", ip, "\t[ICMP Type 8] Echo request")

                self.sock.sendto(packet, (dest_ip, 0))

                response, addr = self.sock.recvfrom(1024)

                print(self.interface.decode("utf-8"), "<-", len(response), "\t\tIP: ", addr[0] if len(addr) else addr, "\t[ICMP Type 0] Echo reply", "\n" + "*" * 60 + "\n")

                cont += 1

                sleep(self.interval)

        except Exception as er:
            print("-------Exception----->", er)

        finally:
            self.sock.close()


# Testing
if __name__ == "__main__":
    try:
        print("\033[2J")
        description = "\tPacket crafting.\nSock RAW ICMP Type 8 ECHO REQUEST"
        epilog = "by DFT"
        parser = argparse.ArgumentParser(description=description, epilog=epilog)
        parser.add_argument("interface", help='Enter the mode monitor activated wireless interface. Ex.: wlan0')
        parser.add_argument("dest_ip", help='Enter the destination IP address. Ex.: 8.8.8.8')
        args = parser.parse_args()

        i = b'wlan0' if len(args.interface) < 1 else args.interface.encode('utf-8')

        ip = '8.8.8.8' if len(args.dest_ip) < 1 else args.dest_ip

        SockRawIcmp(i).ping(ip)

    except Exception as e:
        print("Exception SockRawIcmp(i).ping(ip)", e)
