import cv2
import os
import math
from pascal_voc_tools import XmlParser


class DataCropper():

    def __init__(self):
        self.xml_path = None
        self.img_path = None
        self.xml_data = {}
        self.img_data  = None
        self.cached_imgs = []
        self.cached_xmls = []
        self.boxes = []


    def load(self, filename):
        #loads the xml and image pair for the specified filename
        #filename should not include the suiffix e.g img0135.jpg and img0135.xml filename should be img0135
        self.xml_path = filename + '.xml'
        self.img_path = filename + '.jpg'

        self.xml_data = XmlParser().load(self.xml_path)['object']
        self.img_data = cv2.imread(self.img_path)
        self.img_height, self.img_width = self.img_data.shape[:2]

        return True


    def max(self, args):
        #returns the maximum difference between the four x1min, x1max, x2min, x2max points
        print(args)
        d1 = abs(int(args[0]) - int(args[2]))
        d2 = abs(int(args[0]) - int(args[3]))
        d3 = abs(int(args[1]) - int(args[2]))
        d4 = abs(int(args[1]) - int(args[3]))
        print("D1 @@@@@: {}".format(d2))
        return max([d1, d2, d3, d4])

    def run(self, img_res, res):
        stackable = False
        horizontal = False
        multiplier = -1
        #img_res is target crop dimension e.g 512x512, square only for now
        #res is the percent +/- around edge cases to go to
        boxes_range = self.get_maxmin()

        boxes_aspect = (boxes_range[1][0] - boxes_range[0][0]) / (boxes_range[1][1] - boxes_range[0][1]) #this is the aspect ratio of the bounding box box min/max

        if boxes_aspect >= 1:
            horizontal = True #decides how we will split up the boxes
            multiplier = 1

        i = math.floor(abs(0.5 + multiplier))
        if (boxes_range[1][i] - boxes_range[0][i]) / (img_res * (1 - 2 * res)) >= 2:
            stackable = True


        for square in range(round(boxes_aspect**multiplier)):
            print('hi')


        return True


    def get_maxmin(self):
        #returns the maximum and the minimum x,y coordinates where bounding boxes exist
        max = [0, 0]
        min = [self.img_width, self.img_height]

        for node in self.xml_data:

            name = node['name']
            box = node['bndbox'] #this box is in dict type, {'xmin': '786', etc}

            if int(box['xmin']) < min[0]:
                min[0] = int(box['xmin'])

            if int(box['ymin']) < min[1]:
                min[1] = int(box['ymin'])

            if int(box['xmax']) > max[0]:
                max[0] = int(box['xmax'])

            if int(box['ymax']) > max[1]:
                max[1] = int(box['ymax'])
        return [min, max]

    def maxmin(self, boxes):
        #returns the maximum and the minimum x,y coordinates where bounding boxes exist
        max = [0, 0]
        min = [self.img_width, self.img_height]

        for node in boxes:

            name = node[0]
            box = node[1] #this box is in dict type, {'xmin': '786', etc}

            if int(box['xmin']) < min[0]:
                min[0] = int(box['xmin'])

            if int(box['ymin']) < min[1]:
                min[1] = int(box['ymin'])

            if int(box['xmax']) > max[0]:
                max[0] = int(box['xmax'])

            if int(box['ymax']) > max[1]:
                max[1] = int(box['ymax'])
        return [min, max]


    def get_boxes(self):
        #return the pure xml bounding box data with just the respective identifier
        boxes = []
        for node in self.xml_data:
            boxes.append([node['name'], node['bndbox']])


        return boxes


    def visualize_group(self, box_group):
        #adds the bounding box to the minmax of a group of bounding boxes, good for visualization
        #results can be seen in lablimg tool
        xp = XmlParser()
        xp.load(self.xml_path)
        maxim = self.maxmin(box_group)
        print("MAXIM : {}".format(maxim))
        xp.add_object('vis', maxim[0][0] , maxim[0][1] , maxim[1][0] , maxim[1][1])
        xp.save(self.xml_path)
        return True

    def find_local(self, boxes, img_res, res):
        #searches for closest bounding box

        results = []
        for box in boxes:
            print("BOX: {}".format(box))
            print("BOX IND: {}".format(box[1]['xmin']))
            sub_result = []
            print('h')
            for ele in boxes:
                print("ELE IND: {}".format(ele[1]['xmin']))
                print("ELEMENT: {}".format(ele))

                dx, dy = self.max([ele[1]['xmin'], ele[1]['xmax'], box[1]['xmin'], box[1]['xmax']]), self.max([ele[1]['ymin'], ele[1]['ymax'], box[1]['ymin'], box[1]['ymax']])
                print('inside before subtraction area')
                if dx < img_res * (1- res) and dy < img_res * (1- res) and (dx + dy) > 0:
                    print('inside subtraction area')

                    sub_result.append(ele)

            results.append(sub_result)




        return results

    def sort_boxes(self, boxes):


    def fit_boxes(self, boxes=self.boxes):

        for box in boxes:









        return True
