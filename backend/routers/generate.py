from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/generate")
async def generate_character_sheet(image: UploadFile = File(...)):
    
    pass