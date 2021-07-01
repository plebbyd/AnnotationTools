from tools import DataCropper
import time
import cv2
import matplotlib
import os
import os.path
from os import path




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
            if pixels >= 300 * 300 and dx/dy >= 0.6 and dx/dy < 1.67:
                a.save_slice(bnds, yt[i], i, 'stfd_640')
            time.sleep(0.01)

