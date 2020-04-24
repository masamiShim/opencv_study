import os

import cv2
import numpy as np

exec_path = os.path.dirname(os.path.abspath(__file__))
video_name = 'IMG_0671.mov'


def m_slice(path, step, ext):
    # 動画の読み込み
    movie = cv2.VideoCapture(path)
    # フレーム数の上限？を取得
    Fs = int(movie.get(cv2.CAP_PROP_FRAME_COUNT))
    # 出力パス
    path_head = f"{exec_path}/images/"
    # 出力するフレームの位置を設定(0からFsまでのstep毎の配列を生成)
    ext_index = np.arange(0, Fs, step)

    for i in range(Fs - 1):
        # 読み込めたかどうか(flag)と読み込んだ際のフレームを取得する
        flag, frame = movie.read()

        # 取得フレーム位置に該当するか判定
        check = i in ext_index

        # 読み込めてなかったら処理しない
        if not flag:
            pass

        # 取得フレームに該当している場合処理
        if check:
            if i < 10:
                path_out = f"{path_head}0000{i}{ext}"
            elif i < 100:
                path_out = f"{path_head}000{i}{ext}"
            elif i < 1000:
                path_out = f"{path_head}00{i}{ext}"
            elif i < 10000:
                path_out = f"{path_head}0{i}{ext}"
            else:
                path_out = f"{path_head}{i}{ext}"

            cv2.imwrite(path_out, frame)
    return


m_slice(f"{exec_path}/video/{video_name}", 50, '.png')
