from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
import traceback
import json

from myapi.config import KAFKA_SETTINGS


class Kafka:

    def __init__(self, bootstrap_servers: list = None, topic=None, key_serializer=None, value_serializer=None,
                 partition=None,
                 group_id=None):
        self.bootstrap_servers = bootstrap_servers or KAFKA_SETTINGS.get("bootstrap_servers")
        self.topic = topic
        self.key_serializer = key_serializer if key_serializer else lambda k: json.dumps(k).encode()
        self.value_serializer = value_serializer if value_serializer else lambda v: json.dumps(v).encode()
        self.partition = partition
        self.group_id = group_id
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            key_serializer=self.key_serializer,
            value_serializer=self.value_serializer
        )
        self.consumer = self.get_consumer()

    def get_consumer(self, topic=None, group_id=None):
        topic = topic or self.topic
        group_id = group_id or self.group_id
        if topic and group_id:
            return KafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=group_id
            )
        else:
            return None

    def producer(self, key, value, topic=None, partition=None):
        topic = topic or self.topic
        partition = partition or self.partition
        future = self.producer.send(
            topic=topic,
            key=key,
            value=value,
            partition=partition
        )
        try:
            future.get(timeout=10)
        except Exception as e:
            traceback.format_exc()

    def consumer(self, topic=None, group_id=None):
        consumer = self.get_consumer(topic, group_id) if topic and group_id else self.consumer
        for message in consumer:
            print(
                "receive, key: {}, value: {}".format(
                    json.loads(message.key.decode()),
                    json.loads(message.value.decode())
                )
            )
