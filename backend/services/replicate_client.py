import httpx
import asyncio
import os
# import replicate
from dotenv import load_dotenv

load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
print(REPLICATE_API_TOKEN)
print("see")
MODEL_VERSION = "0304f7f774ba7341ef754231f794b1ba3d129e3c46af3022241325ae0c50fb99"

POSE_URLS = {
    "front": "https://raw.githubusercontent.com/Evastrings/character-sheet-builder/main/backend/assets/pose_front.png",
    "side":  "https://raw.githubusercontent.com/Evastrings/character-sheet-builder/main/backend/assets/pose_side.png",
    "back":  "https://raw.githubusercontent.com/Evastrings/character-sheet-builder/main/backend/assets/pose_back.png",
}

async def run_single_prediction(pose_url: str, prompt: str) -> str:
    # 1. POST to https://api.replicate.com/v1/predictions
    input_d = {
        "image": pose_url,
        "prompt": prompt
    }
    # 2. Get back a prediction id
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url= "https://api.replicate.com/v1/predictions",
            headers= {"Authorization": f"Bearer {REPLICATE_API_TOKEN}"},
            json={"version": MODEL_VERSION, "input": input_d}
        )
        # 3. Poll GET /predictions/{id} until status == "succeeded"
        prediction_id = response.json()["id"]
        while True:
            output_get = await client.get(
                url= f"https://api.replicate.com/v1/predictions/{prediction_id}",
                headers= {"Authorization": f"Bearer {REPLICATE_API_TOKEN}"}
            )
            
            result = output_get.json() 
            # GET /predictions/{id}
            if result["status"] == "succeeded":
                return result["output"][0]

            elif result["status"] == "failed":
                raise Exception(f"Prediction failed: {result.get('error', 'unknown error')}")
            else:
                await asyncio.sleep(2)


async def generate_views(prompt: str) -> list[str]:
    # Use asyncio.gather() to run run_single_prediction 3 times concurrently
    img_urls = await asyncio.gather(*[run_single_prediction(url, prompt) for url in POSE_URLS.values()])
    # Once for each pose in POSE_URLS
    # Return list of 3 output URLs
    return list(img_urls)