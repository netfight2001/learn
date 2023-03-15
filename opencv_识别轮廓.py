#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
形状识别、图像绘制、图像测量demo，demo展示内容：
1.识别常见形状：三角形、矩形、多边形、圆形
程序思路：
2.绘制图像轮廓
3.计算圆形的坐标和最小包围圆半径
加载带形状的图片，对图片进行预处理，然后识别图片中的几何形状，最后画出图像轮廓、质心位置并写上形状文字
 """
__author__ = "River.Yang"
__date__ = "2021/3/10"
__version__ = "1.0"

from time import sleep
import cv2


def get_contours(img):
    # 灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # 黑白翻转
    mask = 255-binary
    cv2.imshow("mask", mask)
    # 获取轮廓
    contous, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    shape_list = []
    if len(contous) > 0:
        for i, contou in enumerate(contous):
            ellipsis = 0.01 * cv2.arcLength(contou, True)
            approxCurve = cv2.approxPolyDP(contou, ellipsis, True)  # 多边形逼近方法获取轮廓
            shape = len(approxCurve)

            # 求质心位置，画出质心
            mm = cv2.moments(contou)
            if mm['m00'] != 0:
                cx = int(mm['m10'] / mm['m00'])
                cy = int(mm['m01'] / mm['m00'])
            else:
                cx = 0
                cy = 0
            cv2.circle(img, (cx, cy), 2, (0, 255, 255), 3)

            shape_str = ""
            shape_CN = ""
            if shape == 3:
                shape_str = "triangle"
                shape_CN = "三角形"
                cv2.drawContours(img, contous, i, (0, 255, 0), 2)
            elif shape == 4:
                shape_str = "rectangle"
                shape_CN = "矩形"
                cv2.drawContours(img, contous, i, (255, 0, 0), 2)
            elif 4 < shape <= 6:
                shape_str = "polygon"
                shape_CN = "多边形"
                cv2.drawContours(img, contous, i, (255, 255, 0), 2)
            elif shape > 6:
                shape_str = "circle"
                shape_CN = "圆形"
                cv2.drawContours(img, contous, i, (0, 0, 255), 2)
                (x_cor, y_cor), radius = cv2.minEnclosingCircle(contou)
                print("圆形的坐标为：(x:%.1f, y:%.1f), 半径为 r = %.2f" % (x_cor, y_cor, radius))
            else:
                continue
            cv2.putText(img, shape_str, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            # 存储形状信息
            shape_list.append([(cx, cy), shape, shape_str, shape_CN])
    cv2.imshow("find cont", img)
    return shape_list


if __name__ == '__main__':
    image = cv2.imread('2dshape.jpg')
    print(get_contours(image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


