import unittest
from unittest.mock import MagicMock, patch

import pika

from app.messaging.rabbitmq import RabbitMQ


class TestRabbitMQReconnect(unittest.TestCase):
    @patch("app.messaging.rabbitmq.pika.BlockingConnection")
    def test_get_channel_reconnects_when_stream_is_lost(self, blocking_connection_cls):
        first_connection = MagicMock()
        first_connection.is_closed = False
        first_connection.channel.side_effect = pika.exceptions.StreamLostError(
            "Stream connection lost",
            BrokenPipeError(32, "Broken pipe"),
        )

        second_connection = MagicMock()
        second_connection.is_closed = False
        second_connection.channel.return_value = object()

        blocking_connection_cls.side_effect = [first_connection, second_connection]

        rabbitmq = RabbitMQ()
        rabbitmq.connection = first_connection

        channel = rabbitmq.get_channel()

        self.assertIs(channel, second_connection.channel.return_value)
        self.assertEqual(blocking_connection_cls.call_count, 2)


if __name__ == "__main__":
    unittest.main()
