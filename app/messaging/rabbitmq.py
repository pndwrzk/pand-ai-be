import pika
from pika.exceptions import AMQPConnectionError, StreamLostError

from app.core.config import settings


class RabbitMQ:

    def __init__(self):
        self.parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            virtual_host=settings.RABBITMQ_VHOST,
            credentials=pika.PlainCredentials(
                settings.RABBITMQ_USERNAME,
                settings.RABBITMQ_PASSWORD,
            ),
        )
        self.connection: pika.BlockingConnection | None = None
        self._connect()

    def _connect(self) -> None:
        self.connection = pika.BlockingConnection(self.parameters)

    def get_channel(self):
        connection = self.connection

        if connection is None or connection.is_closed:
            self._connect()
            connection = self.connection

        if connection is None:
            raise RuntimeError("RabbitMQ connection could not be established")

        try:
            return connection.channel()
        except (StreamLostError, AMQPConnectionError, OSError):
            if connection.is_open:
                try:
                    connection.close()
                except Exception:
                    pass

            self._connect()
            reconnected_connection = self.connection
            if reconnected_connection is None:
                raise RuntimeError("RabbitMQ connection could not be re-established")

            return reconnected_connection.channel()

    def close(self):
        if self.connection is not None and self.connection.is_open:
            self.connection.close()