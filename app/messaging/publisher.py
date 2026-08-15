import json

import pika

from app.messaging.rabbitmq import RabbitMQ


class Publisher:

    def __init__(
        self,
        rabbitmq: RabbitMQ,
    ):
        self.rabbitmq = rabbitmq

    def publish(
        self,
        exchange: str,
        routing_key: str,
        message: dict,
    ):

        channel = self.rabbitmq.get_channel()

        try:

            channel.exchange_declare(
                exchange=exchange,
                exchange_type="topic",
                durable=True,
            )

            channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(message,default=str),
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent,
                ),
            )

        finally:

            if channel.is_open:
                channel.close()