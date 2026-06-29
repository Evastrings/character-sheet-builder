from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter()

@router.get("/generate")
async def generate_character_sheet(image: UploadFile = File(...)):
    
    return {
        "message": "Yokoso watashi no soul society"
    }