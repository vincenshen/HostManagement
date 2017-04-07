
import paramiko
from concurrent.futures import ThreadPoolExecutor


class ParaServer(object):
    def host_connect(self, host, port, username, pass_word):
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=pass_word)
        self.transport = transport
        return transport

    def ssh_connect(self, hosts):
        host = hosts["ip"]
        port = hosts["port"]
        user_name = hosts["username"]
        pass_word = hosts["password"]
        ssh_client = paramiko.SSHClient()
        ssh_client._transport = self.host_connect(host, port, user_name, pass_word)
        std_in, stdout, stderr = ssh_client.exec_command(self.command)
        if stdout:
            print(host+"\n"+str(stdout.read(), encoding="utf-8"))
        else:
            print(host+"\n"+str(stderr.read(), encoding="utf-8"))

    def ssh_thread(self, hosts, command):
        self.command = command
        t = ThreadPoolExecutor(max_workers=2)
        t.map(self.ssh_connect, hosts)

    def __del__(self):
        self.transport.close()

