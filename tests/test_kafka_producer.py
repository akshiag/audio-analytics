import pytest
from unittest.mock import MagicMock, patch
from app.kafka_producer import KafkaTaskProducer

def test_kafka_connect_success(monkeypatch):
    """Test successful Kafka producer connection."""

    # Patch KafkaProducer class to a MagicMock
    mock_kafka_producer = MagicMock()
    monkeypatch.setattr("app.kafka_producer.KafkaProducer", mock_kafka_producer)

    producer = KafkaTaskProducer()
    producer.connect()

    assert producer._producer is not None
    mock_kafka_producer.assert_called_once()  # Ensure KafkaProducer() was called

def test_kafka_send_task_success(monkeypatch):
    """Test sending a task successfully."""

    # Patch KafkaProducer class to a MagicMock
    mock_producer_instance = MagicMock()
    mock_kafka_producer_class = MagicMock(return_value=mock_producer_instance)
    monkeypatch.setattr("app.kafka_producer.KafkaProducer", mock_kafka_producer_class)

    producer = KafkaTaskProducer()

    # Actually call send_task
    task = {"file_path": "fake/path.wav"}
    producer.send_task(task)

    # Assertions
    mock_producer_instance.send.assert_called_once_with("transcription-tasks", task)
    mock_producer_instance.flush.assert_called_once()

def test_kafka_connect_failure(monkeypatch):
    """Test Kafka connection failure is properly logged and raised."""

    def raise_exception(*args, **kwargs):
        raise Exception("Connection failed!")

    monkeypatch.setattr("app.kafka_producer.KafkaProducer", raise_exception)

    producer = KafkaTaskProducer()

    with pytest.raises(Exception, match="Connection failed!"):
        producer.connect()

