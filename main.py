from tools import DataCropper
import time
import cv2
import matplotlib
import os
import os.path
from os import path
"""
a = DataCropper()

a.load('gates_video5_1320')


print(a.xml_data)
print('@@@@@@')
print(a.img_data)
print('@@@@@@@@@')
y = a.get_maxmin()
print('Maxmin: {}'.format(y))

c = a.get_boxes()
for item in c:
    item.append(False)
print(c)
print('QQQQQQQQQQ')

yt = a.find_local(c, 512, .1)
b1 = yt[0]

print("YT : {}".format(yt))

print("GROUPS:")

print(len(yt))
for i in range(len(yt)):
    print(i)
    bigbox = a.maxmin(yt[i])
    print('bigbox i: {}'.format(bigbox))
    a.visualize_group(yt[i])
    dict_format = [['vis', {'xmin': bigbox[0][0], 'ymin': bigbox[0][1], 'xmax': bigbox[1][0], 'ymax': bigbox[1][1]}]]
    print('dict format: {}'.format(dict_format))
    bnds = a.get_bounds(dict_format, upscaling=1.0, offset=0.0)
    print('bnds: {}'.format(bnds))

    a.save_slice(bnds, yt[i], i, 'testslice')
    time.sleep(0.1)
"""

imdir = 'images/train'
a = DataCropper()
test_im = cv2.imread('bookstore_video0_240.jpg')
a.tile(test_im, 3, 4)
'''
for obj in os.listdir(imdir):
    if  not obj.endswith('.xml') and path.exists(imdir + '/' + obj.replace('.jpg','.xml')):
        a = DataCropper()

        a.load(imdir + '/' + obj.replace('.jpg', '').replace('.JPG', ''))
        y = a.get_maxmin()
        c = a.get_boxes()
        a.boxes = c
        for item in c:
            item.append(False)


        yt = a.find_local(c, 640, .1)
        b1 = yt[0]

        for i in range(len(yt)):
            print(i)
            bigbox = a.maxmin(yt[i])
            dict_format = [['vis', {'xmin': bigbox[0][0], 'ymin': bigbox[0][1], 'xmax': bigbox[1][0], 'ymax': bigbox[1][1]}]]
            bnds = a.get_bounds(dict_format, upscaling=1.05, offset=20.0)
            dx, dy = bigbox[1][0] - bigbox[0][0], bigbox[1][1] - bigbox[0][1]
            pixels = dx * dy
            #print('PIXELS: {}'.format(pixels))
            #print('dx and dy: {}'.format(dx) + ' {}'.format(dy))
            if pixels >= 300 * 300 and dx/dy >= 0.6 and dx/dy < 1.67:
                a.save_slice(bnds, yt[i], i, 'stfd_640')
            time.sleep(0.01)
'''
