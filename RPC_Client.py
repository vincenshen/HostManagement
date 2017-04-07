#!/usr/bin/python3
import pika
import subprocess

rabbitmq = {
    "host": "192.168.20.181",
    "exchange": "rpc_exchange2",
    "exchange_type": "direct",
    "routing_key": "192.168.20.181"
}

conn = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq["host"]))
channel = conn.channel()
channel.exchange_declare(exchange=rabbitmq["exchange"], exchange_type=rabbitmq["exchange_type"])
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange=rabbitmq["exchange"], routing_key=rabbitmq["routing_key"], queue=queue_name)


def on_request(ch, method, properties, body):
    res = subprocess.getoutput(str(body, encoding="utf-8"))
    ch.basic_publish(exchange=rabbitmq["exchange"],
                     routing_key=properties.reply_to,
                     body=res)

channel.basic_consume(on_request, queue=queue_name, no_ack=True)
channel.start_consuming()
