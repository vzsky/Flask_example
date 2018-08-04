import urllib
import socket
import telnetlib

Telnet = telnetlib.Telnet

def check(host, port):

    try:
        tn = telnetlib.Telnet(host, port, 3)
        res = 'opened'
    except socket.timeout:
        res = 'timeout'
    except socket.error:
        res = 'closed'

    c={'closed':'danger','timeout':'warning','opened':'success','success':'success'}
    col = c.get(res, 'primary')

    return res, col

def scan(host):
    """Scan every popular ports

    if you can't name the service, then don't scan :)
    """

    ports = [
        21,                 # telnet
        22,                 # ssh
        # 23,25,53,
        80,                 # http
        # 110,137,138,139,143,
        443,                # https
        # 445,548,
        587, 993, 995,      # SMTP
        # 1433,1701,1723,
        3306,               # MySQL
        5432,               # postgresql
        # 8008,8448
    ]
    service = ['telnet','ssh','http','https','SMTP','SMTP','SMTP','MySQL','postgresql']
    ar = []
    p = []
    color = []
    for x in ports:
        r, c = check(host,x)
        ar.append(r)
        p.append(x)
        color.append(c)

    return ar, p, color, service
