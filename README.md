# udpcheck

## udp over socks5 简单测试工具

## Dependencies
- python3

- pysocks
```
python -m pip install pysocks==1.7.1
# python3 -m pip install pysocks==1.7.1
```

## NOTE
如果执行出现下述异常信息
```
socket.error: gaierror(11001, 'getaddrinfo failed')
```

请打上diff目录下的patch到pysocks的socks.py文件

## Usage
```
$ python udpchk.py --help
usage: udpchk.py [-h] --server SERVER [--port PORT] [--user username]
                 [--pwd password] [--target target]

Test SOCKS5 UDP support by sending DNS request to target server and receive
response.

optional arguments:
  -h, --help            show this help message and exit
  --server SERVER, -s SERVER
                        IP or domain name of proxy to be tested against UDP
                        support.
  --port PORT, -p PORT  Port of proxy to be tested against UDP support. (DEF
                        1080)
  --user username, -u username
                        Specify username to be used for proxy authentication.
  --pwd password, -k password
                        Specify password to be used for proxy authentication.
  --target target, -t target
                        Send UDP packet to target server over proxy. (DEF
                        8.8.8.8:53)
```

## Reference

[socks5chk](https://github.com/semigodking/socks5chk) by [semigodking](https://github.com/semigodking)