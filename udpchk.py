# udpchk.py - simple tool to test UDP support of SOCKS5 proxy.
# Copyright (C) 2016-2017 Zhuofei Wang <semigodking@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.

import socks
import socket
import sys
import signal


def test_udp(typ, addr, port, user=None, pwd=None, target=None):
    s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)  # Same API as socket.socket in the standard lib
    target_host, target_port = target.split(":")
    try:
        s.set_proxy(socks.SOCKS5, addr, port, False, user, pwd)  # SOCKS4 and SOCKS5 use port 1080 by default
        # Can be treated identical to a regular socket object
        # Raw DNS request

        # https://stackoverflow.com/questions/5649407/hexadecimal-string-to-byte-array-in-python/5682984
        # Capture Packets with Wireshark
        req = bytes.fromhex(
            "2e68012000010000000000010377777706676f6f676c6503636f6d0000010001000029100000000000000c000a0008c449c7cd2ebd851c")
        s.sendto(req, (target_host, int(target_port)))
        s.settimeout(4)
        (rsp, address) = s.recvfrom(4096)
        print(len(rsp))
        if rsp[0] == req[0] and rsp[1] == req[1]:
            print("UDP check passed")
        else:
            print("Invalid response")
    except (KeyboardInterrupt, SystemExit):
        print('Exiting...')
        s.close()
    except socks.ProxyError as e:
        print("socks.ProxyError:", e.msg)
    except socket.error as e:
        print("socket.error:", repr(e))


def main():
    import os
    import argparse

    def ip_port(string):
        value = int(string)
        if value <= 0 or value > 65535:
            msg = "%r is not valid port number" % string
            raise argparse.ArgumentTypeError(msg)
        return value

    parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                     description='Test SOCKS5 UDP support by sending DNS request to target server and receive response.')
    parser.add_argument('--server', "-s",  metavar="SERVER", dest='server', required=True,
                        help='IP or domain name of proxy to be tested against UDP support.')
    parser.add_argument('--port', "-p",  metavar="PORT", dest='port', type=ip_port, default=1080,
                        help='Port of proxy to be tested against UDP support. (DEF 1080)')
    parser.add_argument('--user', "-u", metavar="username", dest="user", default=None,
                        help='Specify username to be used for proxy authentication.')
    parser.add_argument('--pwd', "-k", metavar="password", dest="pwd", default=None,
                        help='Specify password to be used for proxy authentication.')
    parser.add_argument('--target', "-t", metavar="target", dest="target", default="8.8.8.8:53",
                        help='Send UDP packet to target server over proxy. (DEF 8.8.8.8:53)')
    args = parser.parse_args()
    test_udp(None, args.server, args.port, args.user, args.pwd, args.target)


if __name__ == "__main__":
    main()
