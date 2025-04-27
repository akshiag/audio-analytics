import asyncio
import json
import logging
import os
from kafka import KafkaConsumer
from app.db import get_db_commit
from app.services.transcription_service import process_audio_and_save

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("consumer_worker")

# Kafka setup
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
TOPIC_NAME = "transcription-tasks"

def get_consumer():
    return KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=[KAFKA_BROKER_URL],
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        enable_auto_commit=True,
        group_id="audio-transcriber-group"  # same group ensures no duplication
    )

async def consume_tasks():
    consumer = get_consumer()

    logger.info("Consumer started and listening for tasks...")


    for message in consumer:
        task = message.value
        file_path = task.get("file_path")

        if not file_path:
            logger.warning("No file_path in message, skipping.")
            continue

        logger.info(f"Received task for file: {file_path}")

        db_gen = get_db_commit()
        db = next(db_gen)
        try:
            await process_audio_and_save(db, file_path)
            logger.info(f"Successfully processed and saved: {file_path}")
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to process {file_path}: {e}")
        finally:
            db.close()

if __name__ == "__main__":
    asyncio.run(consume_tasks())
