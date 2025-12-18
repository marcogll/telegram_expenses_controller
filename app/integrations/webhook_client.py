"""
Client for sending data to external webhook URLs.
"""
import httpx
import logging

logger = logging.getLogger(__name__)

async def send_to_webhook(url: str, data: dict):
    """
    Sends a POST request with JSON data to a specified webhook URL.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
            logger.info(f"Successfully sent data to webhook {url}")
            return True
    except httpx.RequestError as e:
        logger.error(f"Failed to send data to webhook {url}: {e}")
        return False
