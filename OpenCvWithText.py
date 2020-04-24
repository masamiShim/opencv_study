import os

from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np

exec_path = os.path.dirname(os.path.abspath(__file__))
image_name = 'images/00000.png'


def img_add_msg(img, message):
    # フォント作成
    font_path = '/Library/Fonts/Arial Unicode.ttf'
    font_size = 24
    font = ImageFont.truetype(font_path, font_size)

    # イメージをPillowに変換
    image = Image.fromarray(img)
    draw = ImageDraw.ImageDraw(image)

    # テキスト描画
    draw.text((50, 50), message, font=font, fill=(255, 255, 255, 0))

    # テキスト追加したものを配列に再変換
    return np.array(image)


_img = cv2.imread(f"{exec_path}/{image_name}")
_message = '新歩一　心結'
converted = img_add_msg(_img, _message)

cv2.imshow('title', converted)
cv2.waitKey(0)
cv2.destroyAllWindows()
