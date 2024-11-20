import logging
import whisper
import os
import uvicorn
from fastapi import FastAPI, Request
import base64

app = FastAPI()
logger = logging.getLogger('uvicorn.error')

@app.post("/")
async def transctibe_file(request: Request):
    json_request = await request.json()
    logger.debug("New request")
    file_data = json_request["file"]
    file_name = json_request["name"]
    file_path = os.path.join("./", file_name)
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(file_data))
    return {"text": transcribe(file_path)}
    #return {'text': 'test1234'}

def transcribe(audio_path: str) -> str:
    whisper_model = os.environ.get('WHISHER_MODEL')
    if whisper_model is None:
        whisper_model = 'turbo'
    model = whisper.load_model(whisper_model)
    try:
        result = model.transcribe(audio_path)
    except Exception as e:
        logger.error(e)
        return 'Error transcribing audio'
    try:
        os.remove(audio_path)
    except:
        pass
    return result["text"]

if __name__ == "__main__":
    logger.debug("Starting server")
    uvicorn.run("main:app", host="0.0.0.0", port=8001, workers=2, use_colors=True, log_level='debug')