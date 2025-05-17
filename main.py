from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import numpy as np
import tensorflow as tf
import shutil
import os
import io

app = FastAPI()

# TODO: 사용해야할 모델이 여러가지라면 어떻게 해야하지? -> 요청 처리 함수 안에서 로드한다면 성능 문제가 발생할 것임.
model = tf.keras.models.load_model("models/nsfw/nsfw_mobilenet2.224x224.h5", compile=False)
model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=1e-6), loss='categorical_crossentropy')

@app.get("/")
def read_root():
    return { "data": "Hello World!" }


@app.post("/nsfw-check")
async def nsfw_check(file: UploadFile = File(...)):
    # 카테고리 이름 (모델에 따라 다를 수 있음)
    # TODO: 잔인하거나 폭력적이거나 Gore한 이미지 분류는 없음..
    CLASSES = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']
    
    try:

        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        image = image.resize((224, 224))

        # numpy array로 변환 및 정규화 (0~1 범위)
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # (1, 224, 224, 3)

        # 모델 추론
        predictions = model.predict(img_array)[0]  # (5,) 배열

        # 예측 결과 정리
        result = {
            "predictions": {CLASSES[i]: float(predictions[i]) for i in range(len(CLASSES))},
            "top_class": CLASSES[int(np.argmax(predictions))],
            "nsfw": CLASSES[int(np.argmax(predictions))] in ["porn", "hentai", "sexy"],
        }

        return result

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))