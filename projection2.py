# -*- encode:utf-8 -*-
import numpy as np
from PIL import Image, ImageOps

def begin():
    # 画像の準備
    gray_img = Image.open("input.pgm").convert('L')

    # 縦横1.5倍にした画像を準備
    orig_x, orig_y = gray_img.size
    b_img = Image.new('L', (round(orig_x * 1.5), round(orig_y * 1.5)))
    ext_x, ext_y = b_img.size
    rev_img = b_img
    b_img.paste(gray_img, (round((ext_x-orig_x)/2), round((ext_y-orig_y)/2)))

    # 回転ステップ数
    rotation_step = 360

    # 投影
    arr = projection(b_img, rotation_step)
    Image.fromarray(np.uint8(arr)).save('sinogram.pgm')

    # 逆投影
    rev_img = rev_projection(rev_img, rotation_step, arr)
    rev_img.save('output.pgm')

    return


def projection(img, rotation_step):
    # 画像を回転させ投影した際の配列をreturn
    arr = []
    for rot in range(rotation_step):
        arr.append(projection_sub(img, rot * (180 / rotation_step)))
        
    return arr

def projection_sub(img, rotation):
    # NEARESTで画像回転 計算した配列をreturn
    rotate_img = img.rotate(rotation, Image.NEAREST)
    arr = np.sum(rotate_img, axis=0)
    arr = arr / img.height
    
    return arr

def rev_projection(img, rotation_step, arr):
    # 逆投影し画像生成
    imgArray = np.zeros((img.height,img.width), dtype=int)

    for r in range(rotation_step):
        appendArray = np.zeros((0,img.width), dtype='uint8')
        for _ in range(img.height):
            appendArray = np.append(appendArray, [arr[r]], axis=0)
        
        # 一旦画像化し回転，配列に戻し加算
        appendImg = Image.fromarray(np.uint8(appendArray)).rotate(r * (180 / rotation_step), Image.NEAREST)
        appendImg.save(str(r) + '.pgm')
        imgArray = imgArray + np.asarray(appendImg)

    # 画像化処理
    imgArray = imgArray / (imgArray.max() / 255)
    outImage = Image.fromarray(np.uint8(imgArray))

    return ImageOps.flip(outImage)


if __name__ == '__main__':
    begin()
