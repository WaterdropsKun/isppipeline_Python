
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math



def mono_image_show(image, width, height,compress_ratio=1):
    x = width/(compress_ratio*100)
    y = height/(compress_ratio*100)
    plt.figure(num='test', figsize=(x, y))
    plt.imshow(image, cmap='gray', interpolation='bicubic', vmax=1.0)
    plt.xticks([]), plt.yticks([])  # 隐藏 X轴 和 Y轴的标记位置和labels
    plt.show()

#显示RGB图像
def rgb_image_show(image, width, height,compress_ratio=1):
    x = width/(compress_ratio*100)
    y = height/(compress_ratio*100)
    plt.figure(num='test', figsize=(x, y))
    plt.imshow(image, interpolation='bicubic', vmax=1.0)
    plt.xticks([]), plt.yticks([])  # 隐藏 X轴 和 Y轴的标记位置和labels
    plt.show()

def ycbcr_compress(image, width, height):
    image[:, :, 0]=image[:,:,0]*219/255+16
    image[:, :, 0] = np.clip(image[:, :, 0], 16, 235)
    image[:, :, 1]=image[:,:,1]*224/255+16
    image[:, :, 1] = np.clip(image[:, :, 1], 16, 240)
    image[:, :, 2]=image[:,:,2]*224/255+16
    image[:, :, 2] = np.clip(image[:, :, 2], 16, 240)
    return image
def ycbcr_decompress(image, width, height):
    image[:, :, 0]=(image[:,:,0]-16)*255/219
    image[:, :, 1]=(image[:,:,1]-16)*255/224
    image[:, :, 2]=(image[:,:,2]-16)*255/224
    image = np.clip(image, 0, 255)
    return image
# 0~255 的 Ycbcr转换
def ycbcr2rgb(image, width, height):
    rgb_img = np.zeros(shape=(height, width, 3))
    rgb_img[:,:,0]=image[:,:,0]+1.402*(image[:,:,2]-128) #R= Y+1.402*(Cr-128)
    rgb_img[:,:,1]=image[:,:,0]-0.344136*(image[:,:,1]-128)-0.714136*(image[:,:,2]-128)#G=Y-0.344136*(Cb-128)-0.714136*(Cr-128)
    rgb_img[:,:,2]=image[:,:,0]+1.772*(image[:,:,1]-128) #B=Y+1.772*(Cb-128)
    rgb_img=np.clip(rgb_img, 0, 255)
    return rgb_img

def ycbcrshow(image, width, height):
    imagergb=ycbcr2rgb(image, width, height)
    rgb_image_show(imagergb, width, height)

def read_NV12_8_file(filename,width,height):
    #文件长度
    image_bytes=int(width*height*3/2)
    #读出文件
    frame = np.fromfile(filename, count=image_bytes,dtype ="uint8")
    framesize = height * width * 3 // 2  # 一帧图像所含的像素个数
    #算出一半高一半款
    h_h = height // 2
    h_w = width // 2

    Yt = np.zeros(shape=(height, width))
    Cb = np.zeros(shape=(h_h, h_w))
    Cr = np.zeros(shape=(h_h, h_w))
    #读取之后直接做reshape
    Yt[:, :] = np.reshape(frame[0:width*height],newshape=(height,width))
    Cb[:, :] = np.reshape(frame[width * height:image_bytes:2], newshape=(h_h, h_w))
    Cr[:, :] = np.reshape(frame[width * height+1:image_bytes:2], newshape=(h_h, h_w))
    #由420扩展到444
    Cb=Cb.repeat(2, 0)
    Cb=Cb.repeat(2, 1)
    Cr=Cr.repeat(2, 0)
    Cr=Cr.repeat(2, 1)
    #拼接到Ycbcr444
    img = np.zeros(shape=(height, width,3))
    img[:,:,0]= Yt[:, :]
    img[:,:,1]= Cb[:, :]
    img[:,:,2]= Cr[:, :]
    return img


if __name__ == '__main__':
    img= read_NV12_8_file(filename='NV12_1920(1920)x1080.yuv', height=1080, width=1920)
    print(np.max(img),np.min(img))
    #img =ycbcr_compress(img, height=1080, width=1920)
    #img=ycbcr_decompress(img, height=1080, width=1920)
    rgb=ycbcr2rgb(img, height=1080, width=1920)

    rgb_image_show(rgb/255, height=1080, width=1920, compress_ratio=1)
