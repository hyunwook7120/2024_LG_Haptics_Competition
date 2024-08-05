from fastapi import File, UploadFile, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from app.routes.model import stt, generate_response

import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def sanitize_filename(filename: str) -> str:
    return filename.replace(":", "_").replace(" ", "_")


@router.post("/upload")
async def upload_file(audioFile: UploadFile = File(...), imageFile: UploadFile = File(...)):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # 오디오 파일 저장
    sanitized_audio_filename = sanitize_filename(f"audio_{audioFile.filename}")
    audio_file_path = os.path.join(upload_dir, sanitized_audio_filename)
    with open(audio_file_path, "wb") as f:
        f.write(await audioFile.read())

    # 이미지 파일 저장
    sanitized_image_filename = sanitize_filename(f"image_{imageFile.filename}")
    image_file_path = os.path.join(upload_dir, sanitized_image_filename)
    with open(image_file_path, "wb") as f:
        f.write(await imageFile.read())

    # 음성 인식 수행
    text = stt(audio_file_path)

    # 모델 결과를 사용하여 응답 생성
    model_result = {'palette_num': "Palette1"}
    print(text)
    result = generate_response(model_result, text)
    print(f"모델 출력: {result}")
    
    return JSONResponse(content={"message": "Uploaded successfully", "text": text})

@router.get("/hyunwook")
async def client(request: Request):
    return templates.TemplateResponse("hyunwook.html", {"request": request})
