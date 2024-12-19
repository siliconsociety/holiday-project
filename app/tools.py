import json

from PIL import Image


def resize_logo(logo_path: str, output_path: str, size: tuple[int, int]) -> None:
    with Image.open(logo_path) as logo:
        resized_logo = logo.resize(size, Image.LANCZOS)
        resized_logo.save(output_path, "WEBP")


def save_json(filename: str, data: dict):
    filepath = f"app/images/{filename}.json"
    with open(filepath, "w") as file:
        json.dump(data, file)  # type: ignore


if __name__ == "__main__":
    resize_logo(
        logo_path="app/assets/logo_256.webp",
        output_path="app/assets/logo_64.webp",
        size=(64, 64)
    )
