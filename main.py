import os
import base64
import cv2
import numpy as np
from PIL import Image

from fastapi import FastAPI, File, UploadFile
app = FastAPI()

# ファイルアップロードでの変換


@app.post("/")
async def face_change(data: UploadFile, target: str = 'esa_agenaide'):
    img = Image.open(data.file)
    result = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    if target == None:
        target = 'esa_agenaide'
    result_image = face_to_image(result, target)
    return {"image": result_image}

# base64からの変換
# FIXME base64文字列が長すぎるのか、受け取り時に途中で切れる模様


@app.post("/base64")
async def face_change(base_image: str, target: str = 'esa_agenaide'):
    np_image = base64_to_cv(base_image)
    if target == None:
        target = 'esa_agenaide'
    result_image = face_to_image(np_image, target)
    return {"image": result_image}


# base64の画像をOpenCVイメージに変換
def base64_to_cv(img_base64: str):
    if "base64," in img_base64:
        # DARA URI の場合、data:[<mediatype>][;base64], を除く
        img_base64 = img_base64.split(",")[1]
    img_data = base64.b64decode(img_base64)
    img_np = np.fromstring(img_data, np.uint8)
    src = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)
    return src


module_dir = os.path.dirname(__file__)  # 一番上のディレクトリ
img_module_dir = os.path.dirname(__file__) + '\image'  # 画像ディレクトリ
cascade_file_path = os.path.join(
    module_dir, 'haarcascade_frontalface_default.xml')  # 顔認識カスケードファイル
cascade = cv2.CascadeClassifier(cascade_file_path)


# 渡された画像の顔を認識し、顔の位置に設定した名前の画像を重ねる
def face_to_image(image_item, target: str):
    frame = image_item
    aveSize = 0
    count = 0
    image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    facerect = cascade.detectMultiScale(
        image_gray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))  # 顔の範囲を取得
    # 顔を検出した場合
    try:
        img_file_path = os.path.join(img_module_dir, (target + '.png'))
        faceImg = cv2.imread(img_file_path, cv2.IMREAD_UNCHANGED)  # 画像
        if len(facerect) > 0:
            for rect in facerect:
                count += 1
                if count < 4:
                    aveSize += (rect[2] + rect[3]) / 2
                    # break
                elif count == 4:
                    aveSize += (rect[2] + rect[3]) / 2
                    aveSize /= 5
                else:
                    aveSize = aveSize * 0.8 + rect[2] * 0.1 + rect[3] * 0.1
                thresh = aveSize * 0.95  # 移動平均の95%以上を閾値
                if rect[2] < thresh or rect[3] < thresh:
                    break
                # 検出した顔を囲む矩形の作成
                # color = (255, 100, 100)
                # cv2.rectangle(frame, tuple(rect[0:2]), tuple( rect[0:2]+rect[2:4]), color, thickness=2)
                faceImg = cv2.resize(
                    faceImg, ((int)(rect[2] * 1.3), (int)(rect[3] * 1.3)), cv2.IMREAD_UNCHANGED)
                rect[0] -= rect[2] * 0.15  # x_offset
                rect[1] -= rect[3] * 0.15  # y_offset
                # 顔の部分に画像挿入
                # FIXME 顔を大きく近づけたり、画面端に顔があるとエラー
                #      おそらく表示している画面の範囲を顔の認識部分が超えてしまったことによる
                #      強制終了する訳では無いが、エラー中は重ねる画像は出ない
                frame[rect[1]:rect[1] + faceImg.shape[0], rect[0]:rect[0] + faceImg.shape[1]] = frame[rect[1]:rect[1] + faceImg.shape[0],
                                                                                                      rect[0]:rect[0] + faceImg.shape[1]] * (1 - faceImg[:, :, 3:] / 255) + faceImg[:, :, :3] * (faceImg[:, :, 3:] / 255)
        ret, image = cv2.imencode(".jpg", frame)
        result_image = base64.b64encode(image).decode("ascii")
        return result_image
    except:
        print('=== getFrames() エラー内容 ===')
        import traceback
        traceback.print_exc()  # エラー表示
        print('=============================')
        ret, image = cv2.imencode(".jpg", frame)
        return False
