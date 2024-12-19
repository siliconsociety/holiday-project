from typing import Literal
from pydantic import BaseModel, Field

ImageSize = Literal["1024x1024", "1792x1024", "1024x1792"]
ImageQuality = Literal["standard", "hd"]
ImageType = Literal["png", "jpg"]


class ImageParams(BaseModel):
    prompt: str = Field("Festive holiday fireplace", description="Prompt for image generation")
    size: ImageSize = Field("1024x1024", description="Image size")
    # quality: ImageQuality = Field("standard", description="Image quality")
    filename: str = Field("image.png", description="Download file name")
    # image_type: ImageType = Field("png", description="Output image format (png or jpg)")
