### Author: Navin Parmar
### COMP 8005 - Final Project

import yaml
import socket
from ipaddress import ip_address, IPv4Address
import sys
from multiprocessing import Process
import _thread

""" Stores processes """
processes = []

with open('conf.yml','r') as f:
    """ Reads config file """
    conf = yaml.safe_load(f.read())
    conf = dict(conf)
    conf=list(conf.values())


def main():
    """ Creates process for each line in configuration file """
    for i in conf:
        p = Process(target=process_setup, args=(i,))
        processes.append(p)
    for i in processes:
        i.start()
    for j in processes:
        j.join()


def process_setup(arr):
    """ This function will be removed. Was originally included due to asyncio """
    conn(arr)


def tunnel(receive, send):
    """Receives and forwards data between sockets """
    while True:
        try:
            data = receive.recv(4096)
            send.send(data)
        except Exception as e:
            print(e)
            break
    try:
        receive.close()
        send.close()
    except Exception as e:
        print("Socket error")




def tunnel_sock(arr):
    """Creates socket and connects to end server"""
    try:
        if type(ip_address(arr[1])) is IPv4Address:
            remote_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            remote_sock.connect((arr[1],int(arr[2])))
            return remote_sock
        else:
            for res in socket.getaddrinfo(arr[1], int(arr[2]), socket.AF_UNSPEC, socket.SOCK_STREAM):
                af, socktype, proto, canonname, sa = res
                try:
                    remote_sock = socket.socket(af, socktype, proto)
                except OSError as msg:
                    sys.exit(msg)
                try:
                    remote_sock.connect(sa)
                    return remote_sock
                except OSError as msg:
                    remote_sock.close()
    except ValueError:
        print('Invalid IP Address. Check configuration')


def conn(config):
    """Listens for connections to be forwarded. Calls relevant functions"""
    arr = config.split("!")
    try:
        addr = ("", int(arr[0]))
        if socket.has_dualstack_ipv6():
            s = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
            while True:
                print("Waiting for connections")
                conn, addr = s.accept()
                print(f"Accepted connection from:{addr}")
                remote_sock = tunnel_sock(arr)
                if remote_sock is None:
                    print('Socket error, check configuration file for remote addr and port')
                else:
                    print(f"Remote Socket Created: {remote_sock}")
                    _thread.start_new_thread(tunnel, (conn, remote_sock))
                    _thread.start_new_thread(tunnel, (remote_sock, conn))
                    print("Data tunnel established")
        else:
            sys.exit('System does not support IPv6 functionality')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()


