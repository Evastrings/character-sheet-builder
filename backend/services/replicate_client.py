import httpx
import asyncio
import os
import replicate
from dotenv import load_dotenv

load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
print(REPLICATE_API_TOKEN)
MODEL_VERSION = "0304f7f774ba7341ef754231f794b1ba3d129e3c46af3022241325ae0c50fb99"

POSE_URLS = {
    "front": "https://raw.githubusercontent.com/Evastrings/character-sheet-builder/main/backend/assets/pose_front.png",
    "side":  "https://raw.githubusercontent.com/Evastrings/character-sheet-builder/main/backend/assets/pose_side.png",
    "back":  "https://raw.githubusercontent.com/Evastrings/character-sheet-builder/main/backend/assets/pose_back.png",
}

async def run_single_prediction(pose_url: str, prompt: str) -> str:
    # 1. POST to https://api.replicate.com/v1/predictions
    #    with the correct JSON body and Authorization header
    input_d = {
        "image": pose_url,
        "prompt": prompt
    }
    # 2. Get back a prediction id
    async with httpx.AsyncClient as client:
        response = await client.post(
            url= "https://api.replicate.com/v1/predictions",
            headers= {"Authorization": f"Bearer {REPLICATE_API_TOKEN}"},
            json={"version": MODEL_VERSION, "input": input_d}
        )
    # 3. Poll GET /predictions/{id} until status == "succeeded"
    # url_id = await output_pred.id
    prediction_id = response.json()[id]
    output_get = client.get(
        url= f"https://api.replicate.com/v1/predictions/{prediction_id}",
        headers= f"Authorization: Bearer {REPLICATE_API_TOKEN}",

    )
    while True:
        output_get = client.get(
            url= f"https://api.replicate.com/v1/predictions/{prediction_id}",
            headers= f"Authorization: Bearer {REPLICATE_API_TOKEN}"
        )
        # GET /predictions/{id}
        if output_get.status == "succeeded":
            break

        elif output_get.status == "failed":
            raise httpx.TimeoutException
        else:
            await asyncio.sleep(2)
            

    # 4. Return the output URL (output is a list, return index 0)
    return output_get[0].url


async def generate_views(prompt: str) -> list[str]:
    # Use asyncio.gather() to run run_single_prediction 3 times concurrently
    img_urls = await asyncio.gather(*[run_single_prediction(url, prompt) for url in POSE_URLS.values()])
    # Once for each pose in POSE_URLS
    # Return list of 3 output URLs
    return list(img_urls)
    


# async def upload_image(image_bytes: bytes, filename: str) -> str:
#     """
#     Upload raw image bytes to Replicate's file upload endpoint.
#     Returns a public URL string.
#     Docs: POST https://api.replicate.com/v1/files
#     """
#     pass


# async def generate_views(image_url: str) -> list[str]:
#     """
#     Fire 3 concurrent ControlNet predictions using the public image URL.
#     Poll each until status == 'succeeded'.
#     Returns a list of 3 output image URLs: [front, side, back]
#     """
#     pass

# import asyncio
# import httpx
# import os
# from dotenv import load_dotenv

# load_dotenv()

# REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
# MODEL_VERSION = "0304f7f774ba7341ef754231f794b1ba3d129e3c46af3022241325ae0c50fb99"

# POSE_URLS = { ... }

# async def run_single_prediction(pose_url: str, prompt: str) -> str:
#     # 1. POST to https://api.replicate.com/v1/predictions
#     #    with the correct JSON body and Authorization header
#     # 2. Get back a prediction id
#     # 3. Poll GET /predictions/{id} until status == "succeeded"
#     # 4. Return the output URL (output is a list, return index 0)
    # pass

# # To access the file URLs:
# print(output[0].url)
# #=> "https://replicate.delivery/.../output_0.png"

# # To write the files to disk:
# for index, item in enumerate(output):
#     with open(f"output_{index}.png", "wb") as file:
#         file.write(item.read())
# #=> output_0.png, output_1.png written to disk
# prompt = "user_prompt"