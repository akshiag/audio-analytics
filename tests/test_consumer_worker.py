import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.consumer_worker import consume_tasks

@pytest.mark.asyncio
async def test_consume_tasks_success(monkeypatch):
    """Test successful consumption of a task."""

    # --- Mocks ---
    fake_message = MagicMock()
    fake_message.value = {"file_path": "tests/resources/harvard.wav"}

    fake_consumer = [fake_message]

    # Patch KafkaConsumer
    monkeypatch.setattr("app.consumer_worker.get_consumer", lambda: fake_consumer)

    # Patch process_audio_and_save to be AsyncMock
    fake_process_audio_and_save = AsyncMock()
    monkeypatch.setattr("app.consumer_worker.process_audio_and_save", fake_process_audio_and_save)

    # Patch get_db_commit to yield a mock db session
    fake_db = MagicMock()
    monkeypatch.setattr("app.consumer_worker.get_db_commit", lambda: iter([fake_db]))

    # --- Run ---
    await asyncio.wait_for(consume_tasks(), timeout=1)

    # --- Assertions ---
    fake_process_audio_and_save.assert_called_once_with(fake_db, "tests/resources/harvard.wav")
    fake_db.close.assert_called_once()

