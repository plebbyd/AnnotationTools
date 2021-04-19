import cv2
import os
import math
from pascal_voc_tools import PascalXml


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
        self.img_data = cv2.imread(r'{}'.format(self.img_path))
        self.img_height, self.img_width = self.img_data.shape[:2]

        return True


    def max(self, args):
        #returns the maximum difference between the four x1min, x1max, x2min, x2max points
        #print(args)
        d1 = abs(int(args[0]) - int(args[2]))
        d2 = abs(int(args[0]) - int(args[3]))
        d3 = abs(int(args[1]) - int(args[2]))
        d4 = abs(int(args[1]) - int(args[3]))
        return max([d1, d2, d3, d4])

    def run(self, img_res, res):
        #run will do EVERYTHING for the main filepair (xml, jpg) to be split into the various sub objects
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
            #print("BOX: {}".format(box))
            #print("BOX IND: {}".format(box[1]['xmin']))
            if box[2] is False:
                sub_result = []
                box[2] = True
                print('h')
                sub_result.append(box)
                for ele in boxes:
                    #print("ELE IND: {}".format(ele[1]['xmin']))
                    #print("ELEMENT: {}".format(ele))

                    dx, dy = self.max([ele[1]['xmin'], ele[1]['xmax'], box[1]['xmin'], box[1]['xmax']]), self.max([ele[1]['ymin'], ele[1]['ymax'], box[1]['ymin'], box[1]['ymax']])
                    #print('inside before subtraction area')
                    if dx < img_res * (1- res) and dy < img_res * (1- res) and (dx + dy) > 0:
                        #print('inside subtraction area')
                        if ele[2] is False:
                            print("Element inside appending : {}".format(ele))
                            sub_result.append(ele)
                            ele[2] = True
                if len(sub_result) > 0 and sub_result != results[:]:
                    results.append(sub_result)





        return results

    def area(self, rec1, rec2):
        #returns the area intersected by rectangle 1 and rectangle 2, where rect1 = [xmin, ymin, xmax, ymax]
        dx = min(rec1[2], rec2[2]) - max(rec1[0], rec2[0])
        dy = min(rec1[3], rec2[3]) - max(rec1[1], rec2[1])

        if (dx>0) and (dy>0):
            return dx*dy

    def get_distance(self, rec1, rec2):
        #returns the distance from the centerpoints, where rec1 = [xmin, ymin, xmax, ymax]
        x_avg_1, y_avg_1 = (rec1[0]+rec1[2])/2, (rec1[1]+rec1[3])/2
        x_avg_2, y_avg_2 = (rec2[0]+rec2[2])/2, (rec2[1]+rec2[3])/2
        return int(sqrt((x_avg_1 - x_avg_2)^2 + (y_avg_1 - y_avg_2)^2))

    def consume(self, rec1, rec2, percent=1.0):
        #combines the two rectangles if either is entirely inside the other (or within a set % total area inside, specified by percent input 95% overlap = 0.95)
        rec_1_area = (rec1[3] - rec1[1]) * (rec1[2] - rec1[0])
        rec_2_area = (rec2[3] - rec2[1]) * (rec2[2] - rec2[0])
        if area(rec1,rec2)/rec_1_area > percent or area(rec1,rec2)/rec_2_area > percent:
            return maxmin(rec1, rec2)

    def contest(self):
        #if item bounding boxes are in multiple higher-level boxes, then this method determine which they will go to
        #calculates the distance from the bounding boxes in question to

        return True


    def fit_boxes(self):

        for box in boxes:


            print('hi')


        return True

    def get_bounds(self, boxes, upscaling=1.0, offset=0.0):
        #boxes is meant to be a higher-level bounding box containing lowest level bboxes
        #gets the coordinates for the final image cut, goes out and makes sure it doesn't intersect bboxes outside of the main box. upscaling and offset can be used simultaneously or individually
        #to add extra pixel area arounds the max/min points of the higher level bounding box
        maxim = self.maxmin(boxes)
        dx, dy = maxim[1][0] - maxim[0][0] , maxim[1][1] - maxim[0][1]
        x_min = int(maxim[0][0] - ((upscaling - 1.0)*dx + offset))
        y_min = int(maxim[0][1] - ((upscaling - 1.0)*dy + offset))
        x_max = int(maxim[1][0] + ((upscaling - 1.0)*dx + offset))
        y_max = int(maxim[1][1] + ((upscaling - 1.0)*dy + offset))
        bounds = [0 if x_min < 0 else x_min, 0 if  y_min < 0 else y_min, self.img_width if  x_max > self.img_width else x_max, self.img_height if  y_max > self.img_height else y_max]
        return bounds

    def save_slice(self, box, bboxes, id, save_path):
        #saves an img (jpg) slice of the main image with its respective xml pair
        #box is in the form: [xmin, ymix, xmax, ymax], it should be the higher-level bounding box after being expanded using get_bounds
        #bboxes is all of the xml data for ther boxes inside of the higher level box = box
        #save path is the new filename and path
        width, height = box[2] - box[0], box[3] - box[1]
        cv2.imwrite(save_path + '/' + self.img_path.replace('.jpg','') + 'slice{}'.format(id) + '.jpg', self.img_data[box[1]:box[3], box[0]:box[2]]) #This is [ymin:ymax, xmin:xmax] for some reason
        xp = XmlParser()
        xp.set_head(self.img_path.replace('.jpg','') + 'slice{}'.format(id) + '.jpg', width = width, height = height)
        """
        for b in bboxes:
            print("b @0: {}".format(b[0]))
            new_b = [b[0], int(b[1]['xmin']) - box[0], int(b[1]['ymin']) - box[1], int(b[1]['xmax']) - box[0], int(b[1]['ymax']) - box[1]]

            xp.add_object(new_b[0], new_b[1], new_b[2], new_b[3], new_b[4])
        """
        print('SELF BOXES: {}'.format(self.boxes))
        for ob in self.boxes:
            print("SELF area: {}".format(self.area([int(ob[1]['xmin']), int(ob[1]['ymin']), int(ob[1]['xmax']), int(ob[1]['ymax'])], box)))
            if self.area([int(ob[1]['xmin']), int(ob[1]['ymin']), int(ob[1]['xmax']), int(ob[1]['ymax'])], box) is not None:
                if self.area([int(ob[1]['xmin']), int(ob[1]['ymin']), int(ob[1]['xmax']), int(ob[1]['ymax'])], box) > 0.01:

                    xp.add_object(ob[0], 0 if int(ob[1]['xmin']) < box[0] else int(ob[1]['xmin']) - box[0], 0 if int(ob[1]['ymin']) < box[1] else int(ob[1]['ymin']) - box[1], box[2] - box[0] if int(ob[1]['xmax']) > box[2] else int(ob[1]['xmax']) - box[0], box[3] - box[1] if int(ob[1]['ymax']) > box[3] else int(ob[1]['ymax']) - box[1])




        xp.template_parameters['path'] = xp.template_parameters['path'].replace('\\' , '/')
        print(xp.template_parameters['path'])
        xp.save(save_path + '/' + self.img_path.replace('.jpg','') + 'slice{}'.format(id) + '.xml')

    def tile(self, image, row, col):
        height, width, channels = image.shape

        for i in range(col):
            for j in range(row):
                new_im = image[int(j*(height/row)):int((j+1)*(height/row)),int(i*(width/col)):int((i+1)*width/col)]
                cv2.imwrite(str(j) +str(i) + '.jpg', new_im)
