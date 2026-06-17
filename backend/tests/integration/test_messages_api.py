# =============================================================================
# forge / tests / integration / test_messages_api
# =============================================================================
# Description : Integration tests for conversation message endpoints.
# Layer       : Infra
# Feature     : F005 — Basic Conversation Interface
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import pytest
from httpx import AsyncClient


async def _create_session(client: AsyncClient) -> str:
    """Helper to create a session and return its id."""
    resp = await client.post("/api/sessions", json={})
    return str(resp.json()["id"])


@pytest.mark.asyncio
async def test_send_message_streams_sse(client: AsyncClient) -> None:
    """POST message returns SSE stream with delta and done events."""
    session_id = await _create_session(client)

    async with client.stream(
        "POST",
        f"/api/sessions/{session_id}/messages",
        json={"content": "Hello"},
    ) as response:
        assert response.status_code == 200
        body = ""
        async for chunk in response.aiter_text():
            body += chunk

    assert "data:" in body
    assert '"delta"' in body
    assert '"done"' in body


@pytest.mark.asyncio
async def test_list_and_clear_messages(client: AsyncClient) -> None:
    """Messages can be listed and cleared via REST."""
    session_id = await _create_session(client)
    async with client.stream(
        "POST",
        f"/api/sessions/{session_id}/messages",
        json={"content": "Hi"},
    ) as response:
        async for _ in response.aiter_text():
            pass

    list_resp = await client.get(f"/api/sessions/{session_id}/messages")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 2

    clear_resp = await client.delete(f"/api/sessions/{session_id}/messages")
    assert clear_resp.status_code == 200
    assert clear_resp.json()["removed"] == 2


@pytest.mark.asyncio
async def test_inference_chat_endpoint(client: AsyncClient) -> None:
    """Direct inference chat returns mock completion."""
    response = await client.post(
        "/api/inference/chat",
        json={
            "messages": [{"role": "user", "content": "ping"}],
            "model_alias": "fast",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Mock reply"
    assert data["prompt_tokens"] == 10


@pytest.mark.asyncio
async def test_regenerate_message_stream(client: AsyncClient) -> None:
    """Regenerate endpoint streams a new assistant reply."""
    session_id = await _create_session(client)
    async with client.stream(
        "POST",
        f"/api/sessions/{session_id}/messages",
        json={"content": "Explain"},
    ) as response:
        async for _ in response.aiter_text():
            pass

    async with client.stream(
        "POST",
        f"/api/sessions/{session_id}/messages/regenerate",
    ) as response:
        assert response.status_code == 200
        text = ""
        async for chunk in response.aiter_text():
            text += chunk

    assert '"done"' in text
