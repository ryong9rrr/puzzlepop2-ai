from fastapi import FastAPI, File, UploadFile, HTTPException
#from nsfw_detector import predict
import shutil
import os

app = FastAPI()

model = None

@app.get("/")
def read_root():
    return { "data": "Hello World!" }


@app.post("/nsfw-check")
async def nsfw_check(file: UploadFile = File(...)):

    #model = predict.load_model()

    try:
        print(file)
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": file.size,
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))