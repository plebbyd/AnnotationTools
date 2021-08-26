# AnnotationTools

Annotation tools is used for already annotated image datasets to filter and refine the labels.

Annotation tools can create sub slices of images for better resolution when put into training


Usage:

`dc = DataCropper()`  Creates new DataCropper object, required to use the methods

`dc.load('img0132')` loads the xml and jpg file pair for an annotated image with the name img0132

`dc.max()` returns the maximum value of four differences in distance - used to determine max distance between two bounding boxes

`dc.get_maxmin()` returns the minimum and maximum coordinates for a set of bounding boxes

