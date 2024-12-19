from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.image_kit import generate_image
from app.schema import ImageParams

API = FastAPI(
    title="ImageBot",
    version="1.0.0",
    docs_url="/",
    description="Image Generator Bot",

)
API.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@API.post("/generate", tags=["Image Generator"])
async def generate(params: ImageParams):
    try:
        return FileResponse(
            await generate_image(params),
            media_type=f"image/png",
            filename=params.filename,
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
