import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

exec_path = os.path.dirname(os.path.abspath(__file__))
video_dir = f"{exec_path}{os.path.sep}video{os.path.sep}"
input_video_name = 'IMG_0671.mov'
_step = 1
_output_telop = 'telop_sample.mp4'
_output_tmp_telop = 'telop_tmp.mp4'

_messages = [
]


def sub_color(src, K):
    Z = src.reshape((-1, 3))

    Z = np.float32(Z)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 10, 1.0)

    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)

    res = center[label.flatten()]

    return res.reshape((src.shape))


def mosaic(img, alpha):
    h, w, ch = img.shape

    img = cv2.resize(img, (int(w * alpha), int(h * alpha)))

    img = cv2.resize(img, (w, h), interpolation=cv2.INTER_NEAREST)

    return img

def pixel_art(img, alpha=2, K=4):
    img = mosaic(img, alpha)

    return sub_color(img, K)

def anime_filter(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    edge = cv2.blur(gray, (3, 3))

    edge = cv2.Canny(edge, 50, 150, apertureSize=3)

    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    img = cv2.pyrMeanShiftFiltering(img, 5, 20)

    return cv2.subtract(img, edge)


def rotate_movie(movie, out_path, step):
    fs = int(movie.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = movie.get(cv2.CAP_PROP_FPS)
    w = int(movie.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(movie.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # ?fourrcc???
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    video = cv2.VideoWriter(out_path, fourcc, int(fps / step), (h, w))

    for i in range(fs):
        flag, frame = movie.read()
        video.write(cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE))


def telop(img, message, width, height):
    font_path = '/Library/Fonts/Arial Unicode.ttf'
    font_size = 24
    font = ImageFont.truetype(font_path, font_size)

    # イメージをPillowに変換
    image = Image.fromarray(img)
    draw = ImageDraw.ImageDraw(image)

    w, h = draw.textsize(message, font)

    # 中央揃え
    position = (int((width - w) / 2), int((height - 50) - h))

    draw.text(position, message, font=font, fill=(255, 255, 255, 0))

    drawn = np.array(image)
    return drawn


def m_slice(output, step, messages):
    input_path = f"{video_dir}{input_video_name}"
    out_path = f"{video_dir}{output}"
    out_tmp_path = f"{video_dir}{_output_tmp_telop}"

    base_movie = cv2.VideoCapture(input_path)
    rotate_movie(base_movie, out_tmp_path, step)

    movie = cv2.VideoCapture(out_tmp_path)
    fs = int(movie.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = movie.get(cv2.CAP_PROP_FPS)
    w = int(movie.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(movie.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # ?fourrcc???
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    video = cv2.VideoWriter(out_path, fourcc, int(fps / step), (w, h))
    ext_index = np.arange(0, fs, step)

    j = 0
    section = messages[j]

    for i in range(fs):
        print(i)
        flag, frame = movie.read()
        # frame = pixel_art(frame)
        check = i == ext_index
        time = i / int(fps / step)

        if not flag:
            continue

        if True in check:
            # もしi番目のフレームが静止画を抽出するものであれば、ファイル名を付けて保存する
            if True in check:
                # ここから動画フレーム処理と動画保存---------------------------------------------------------------------
                # 抽出したフレームの再生時間がテロップを入れる時間範囲に入っていれば文字入れする
                if section[1] <= time <= section[2]:
                    frame = telop(frame, section[0], w, h)  # テロップを入れる関数を実行
                # 再生時間がテロップ入れ開始時間より小さければ待機する
                elif section[1] > time:
                    pass
                else:
                    # 用意した文章がなくなったら何もしない
                    if j >= len(messages) - 1:
                        pass
                    # 再生時間範囲になく、まだmessage配列にデータがある場合はjを増分しsectionを更新
                    else:
                        j = j + 1
                        section = messages[j]
                video.write(frame)
    return


m_slice(_output_telop, _step, _messages)
