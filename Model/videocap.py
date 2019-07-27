import os
import cv2
from PIL import Image
from path import Path
import sys
import os
import subprocess
import ffmpeg


def unlock_mv(sp, outputPath):
    output = subprocess.Popen("ffmpeg -i '" + sp + "' -r 1 -q:v 2 -f image2 '" + outputPath + "'%05d.jpg",
                              shell=True,
                              stdout=subprocess.PIPE
                              ).stdout.read()


def jpg2video(sp, fps):
    """ 将图片合成视频. sp: 视频路径，fps: 帧率 """
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    images = os.listdir('/Users/momo/PycharmProjects/subrecog/roiframes/')
    im = Image.open('/Users/momo/PycharmProjects/subrecog/roiframes/' + images[0])
    vw = cv2.VideoWriter(sp, fourcc, fps, im.size)

    os.chdir('/Users/momo/PycharmProjects/subrecog/roiframes/')
    for image in range(len(images)):
        # Image.open(str(image)+'.jpg').convert("RGB").save(str(image)+'.jpg')
        jpgfile = str(image + 1) + '.jpg'
        try:
            frame = cv2.imread(jpgfile)
            vw.write(frame)
        except Exception as exc:
            print(jpgfile, exc)
    vw.release()
    print(sp, 'Synthetic success!')

def video_duration(sp):
    cap = cv2.VideoCapture(sp)
    if cap.isOpened():
        rate = cap.get(5)  # 帧率FPS
        FrameNumber = cap.get(7)  # 帧数
        duration = FrameNumber/rate
    return rate, FrameNumber, duration


if __name__ == '__main__':
    sp = "/Users/momo/testvideo/cutout2.mp4"

    unlock_mv(sp, '/Users/momo/testvideo/')  # 视频转图片
    # sp_new = 'subtitleroi.avi'
    # jpg2video(sp_new, 28)  # 图片转视频
