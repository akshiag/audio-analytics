import json
import logging
import os

from kafka import KafkaProducer
from kafka.errors import KafkaError

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class KafkaTaskProducer:
    """
    A class to manage Kafka producer connections and send tasks to a Kafka topic.
    """

    def __init__(self) -> None:
        """
        Initialize the KafkaTaskProducer instance with a lazy Kafka producer.
        """
        self._producer: KafkaProducer | None = None

    def connect(self) -> None:
        """
        Establish a connection to the Kafka broker and initialize the producer.

        Raises:
            Exception: If the connection to the Kafka broker fails.
        """
        if not self._producer:
            try:
                # Get the Kafka broker URL from the environment variable or use the default
                KAFKA_BROKER_URL: str = os.getenv("KAFKA_BROKER_URL", "localhost:9092")

                # Initialize the Kafka producer
                self._producer = KafkaProducer(
                    bootstrap_servers=[KAFKA_BROKER_URL],
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),#Serialize messages
                    acks="all"  # Wait for acknowledgment from all replicas
                )
                logger.info(f"Kafka producer connected to {KAFKA_BROKER_URL}")
            except Exception as e:
                logger.error(f"Failed to connect Kafka Producer: {e}")
                raise

    def send_task(self, task: dict) -> None:
        """
        Send a task to the Kafka topic 'transcription-tasks'.

        Args:
            task (dict): The task data to be sent to Kafka.

        Raises:
            KafkaError: If there is an error sending the message to Kafka.
            Exception: For any unexpected errors during message sending.
        """
        self.connect()  # Ensure the producer is connected
        try:
            # Send the task to the Kafka topic
            self._producer.send("transcription-tasks", task)
            self._producer.flush()  # Ensure all messages are sent
            logger.info("Task successfully sent to Kafka.")
        except KafkaError as e:
            logger.error(f"Kafka sending error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending Kafka task: {e}")

# Create a lazy instance of KafkaTaskProducer
kafka_task_producer: KafkaTaskProducer = KafkaTaskProducer()