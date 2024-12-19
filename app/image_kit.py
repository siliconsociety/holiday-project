from os import getenv, makedirs, path
import requests
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import HTTPException
from PIL import Image
from uuid import uuid4
from io import BytesIO
from app.schema import ImageParams
from app.tools import save_json

load_dotenv()
client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
IMAGE_DIR = "app/images"
LOGO_PATH = "app/assets/logo_64.webp"
makedirs(IMAGE_DIR, exist_ok=True)


def add_logo_and_save(image_bytes: bytes, output_path: str, image_type: str) -> None:
    padding: int = 20
    with (Image.open(BytesIO(image_bytes)).convert("RGBA")
          as img, Image.open(LOGO_PATH).convert("RGBA") as logo):
        x = img.width - logo.width - padding
        y = img.height - logo.height - padding
        img.paste(logo, (x, y), logo)
        if image_type == "jpg":
            img = img.convert("RGB")
            img.save(output_path, "JPEG")
        else:
            img.save(output_path, "PNG")


async def generate_image(params: ImageParams) -> str:
    response = client.images.generate(
        model="dall-e-3",
        prompt=params.prompt,
        size=params.size,
        quality="hd",
        n=1,
    )
    image_url = response.data[0].url
    image_response = requests.get(image_url)
    if image_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to download the image")
    filename, ext = path.splitext(params.filename)
    image_type = "png"
    name = f"{filename}_{uuid4()}"
    unique_filename = f"{name}.{image_type}"

    data = params.model_dump()
    save_json(name, data)

    final_image_path = path.join(IMAGE_DIR, unique_filename)
    add_logo_and_save(
        image_bytes=image_response.content,
        output_path=final_image_path,
        image_type=image_type,
    )
    return final_image_path


if __name__ == "__main__":
    import asyncio
    params = ImageParams(
        prompt="A futuristic city skyline at sunset on Christmas",
        size=["1024x1024", "1792x1024", "1024x1792"][2],
        quality="standard",
        filename="my_image.png",
        image_type="png"
    )
    output_image = asyncio.run(generate_image(params))
    print(f"Image saved with logo at: {output_image}")
