import httpx
import os
from dotenv import load_dotenv

load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")



async def upload_image(image_bytes: bytes, filename: str) -> str:
    """
    Upload raw image bytes to Replicate's file upload endpoint.
    Returns a public URL string.
    Docs: POST https://api.replicate.com/v1/files
    """
    pass


async def generate_views(image_url: str) -> list[str]:
    """
    Fire 3 concurrent ControlNet predictions using the public image URL.
    Poll each until status == 'succeeded'.
    Returns a list of 3 output image URLs: [front, side, back]
    """
    pass