import time

from HostManage.core.dbconnection import DBConn
from HostManage.core.paraserver import ParaServer
from HostManage.core.rpcserver import RPCServer

# database: hostm
# tables: user_type.dbf users.dbf hosts.dbf user_to_host.dbf
# user: alex 123456


class HostManage(object):
    def __init__(self):
        self.db = DBConn()
        self.para = ParaServer()

    def host_list(self, user):
        return self.db.host(user)

    def auth(self, user, password):
        return self.db.auth(user, password)

    def ssh(self, hosts, command):
        return self.para.ssh_thread(hosts, command)

    def rpc(self, hosts, command):
        for host in hosts:
            rpcserver = RPCServer()
            rpcserver.call(host, command)


def interactive():
    host_manage = HostManage()
    while True:
        username = input("Please input username >>>")
        password = input("Please input password >>>")
        if host_manage.auth(username, password):
            break
        else:
            print("Authentication Failed!")
    host_list = host_manage.host_list(username)
    while True:
        print("Your host list".center(40, "-"))
        for n, k in enumerate(host_list):
            print(n, ":", k["ip"])
        numbers = input("Please choice host number >>>").strip()
        if numbers == "q":
            exit()
        elif len(numbers) == 0:
            continue
        hosts = []
        hosts2 = []
        for num in numbers.split(" "):      # split host list use blankspace
            hosts.append(host_list[int(num)])
            hosts2.append(host_list[int(num)]["ip"])
        command = input("Please input shell command >>>")
        print("1. Paramiko connection mode\n2. RPC connection mode")
        choice = input("Please choice a connection mode >>>")
        if choice == "1":
            host_manage.ssh(hosts, command)
        if choice == "2":
            host_manage.rpc(hosts2,command)


if __name__ == '__main__':
    interactive()