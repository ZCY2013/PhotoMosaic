# coding:utf-8
import cv2
import os
import collections
import numpy as np

# 原图路径
readPath = r"/Users/zhaochangyue/Downloads/CATDATASET/jpg_pak"
# 预处理后图片集路径
savePath = r"/Users/zhaochangyue/Downloads/CATDATASET/after_handle"


def pre_handler():
    # 用一个列表保存所有的图片的文件名字
    files = os.listdir(readPath)

    # n变量用来看到10万张图片的处理进度。
    n = 0

    # 遍历所有图片文件们
    for file in files:
        n += 1
        imgPath = readPath + "/" + file
        img = cv2.imread(imgPath)
        img = cv2.resize(img, (100, 100))

        cv2.imwrite(savePath + "/" + file, img)
        print(n)


def create_index():

    files = os.listdir(savePath)
    n = 0
    s = ''
    for file in files:
        li = []
        n += 1
        imgPath = savePath + "/" + file
        img = cv2.imread(imgPath)
        for i in range(100):
            for j in range(100):
                b = img[i, j, 0]
                g = img[i, j, 1]
                r = img[i, j, 2]
                li.append((b, g, r))

        most = collections.Counter(li).most_common(1)
        s += file
        s += ":"
        s += str(most[0][0]).replace("(", "").replace(")", "")
        s += "\n"
        print(n)

    f = open('filename.txt', 'w')
    f.write(s)


def readIndex():
    fs = open("filename.txt", "r")
    n = 0
    dic = []
    for line in fs.readlines():
        n += 1
        temp = line.split(":")
        file = temp[0]
        bgr = temp[1].split(",")
        b = int(bgr[0])
        g = int(bgr[1])
        r = int(bgr[2])
        dic.append((file, (b, g, r)))
    return dic


def draw_pic():
    file_name = "huge.png"
    target_path = r"/Users/zhaochangyue/Downloads/" + file_name
    img = cv2.imread(target_path)
    s = np.shape(img)
    img = cv2.resize(img, (int(s[1] * 100.0 / s[0]), 100))  # modify height and width
    s = np.shape(img)
    big = np.zeros((100 * s[0], 100 * s[1], 3), dtype=np.uint8)

    list = readIndex()  # 读取索引文件到变量中
    for i in range(s[0]):  # 遍历行和列
        print(i)
        for j in range(s[1]):
            b = img[i, j, 0]
            g = img[i, j, 1]
            r = img[i, j, 2]  # 获取图像当前位置的BGR值

            np.random.shuffle(list)  # 打乱索引文件

            for item in list:
                imgb = item[1][0]
                imgg = item[1][1]
                imgr = item[1][2]  # 获取索引文件的RGB值

                distance = (imgb - b) ** 2 + (imgg - g) ** 2 + (imgr - r) ** 2  # 欧式距离
                if distance < 100:
                    filepath = savePath + "/" + str(item[0])  # 定位到具体的图片文件
                    little = cv2.imread(filepath)  # 读取整个最相近的图片
                    big[i * 100:(i + 1) * 100, j * 100:(j + 1) * 100] = little  # 把图片画到大图的相应位置
                    break
    cv2.imwrite("/Users/zhaochangyue/Documents/huge.jpg", big)  # 输出大图到文件中


if __name__ == '__main__':
    draw_pic()
