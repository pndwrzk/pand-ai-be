import json

from app.messaging.rabbitmq import RabbitMQ


class Consumer:

    def __init__(self, rabbitmq: RabbitMQ):
        self.rabbitmq = rabbitmq

    def consume(
        self,
        exchange: str,
        queue: str,
        routing_key: str,
        callback,
    ):
        print("Getting channel...")
        channel = self.rabbitmq.get_channel()

        print("Declaring exchange...")
        channel.exchange_declare(
            exchange=exchange,
            exchange_type="topic",
            durable=True,
        )

        print("Declaring queue...")
        channel.queue_declare(
            queue=queue,
            durable=True,
        )

        print("Binding queue...")
        channel.queue_bind(
            exchange=exchange,
            queue=queue,
            routing_key=routing_key,
        )

        def wrapper(ch, method, properties, body):
            callback(json.loads(body))
            ch.basic_ack(delivery_tag=method.delivery_tag)

        print("Register consumer...")
        channel.basic_consume(
            queue=queue,
            on_message_callback=wrapper,
        )

        print(f"Listening on {queue}...")
        channel.start_consuming()