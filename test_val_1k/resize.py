#!/Users/cwang/opt/anaconda3/bin/python
import sys
from PIL import Image

# files = ['val/ILSVRC2012_val_00000100.JPEG','val/ILSVRC2012_val_00000222.JPEG']
files = sys.argv[1:]

files.sort()

h = w = 299
count = 0
for each_file in files:

    count += 1
    if count%100 == 0:
        print(count)

    tags = each_file.split("/")
    output_filename = 'resize/'+tags[-1]
    image = Image.open(each_file)
    aspect = w / h
    image_aspect = image.width / image.height

    if image_aspect > aspect:
        # image is wider than our aspect ratio
        new_height = image.height
        height_off = 0
        new_width = int(aspect * new_height)
        width_off = (image.width - new_width) // 2
    else:
        # image is taller than our aspect ratio
        new_width = image.width
        width_off = 0
        new_height = int(new_width / aspect)
        height_off = (image.height - new_height) // 2

    # box is (left, upper, right, lower)
    image = image.crop((
        width_off,
        height_off,
        width_off+new_width,
        height_off+new_height
    ))

    image = image.resize((w, h))
    image.save(output_filename)


