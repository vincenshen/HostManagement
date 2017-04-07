import pika
from HostManage.conf.settings import rabbitmq
from concurrent.futures import ThreadPoolExecutor


class RPCServer(object):
    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq["host"]))
        self.channel = self.conn.channel()
        self.channel.exchange_declare(exchange=rabbitmq["exchange"], exchange_type=rabbitmq["exchange_type"])
        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=rabbitmq["exchange"], routing_key=self.queue_name, queue=self.queue_name)
        self.channel.basic_consume(self.callback, no_ack=True, queue=self.queue_name)

    def callback(self, ch, method, properties, body):
        print(str(body, encoding="utf-8"))
        self.channel.stop_consuming()

    def call(self, host, cmd):
        print(host)
        self.channel.basic_publish(exchange=rabbitmq["exchange"],
                                   routing_key=host,
                                   properties=pika.BasicProperties(reply_to=self.queue_name,),
                                   body=cmd)
        self.channel.start_consuming()


if __name__ == '__main__':
    while True:
        rpc = RPCServer()
        hostname = input("hostname...")
        cmd = input("cmd...")
        rpc.call(hostname, cmd)