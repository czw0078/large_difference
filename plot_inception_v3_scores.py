# stack overflow reference
# https://stackoverflow.com/questions/35737116/runtimeerror-invalid-display-variable
import matplotlib
matplotlib.use('agg')

import os
import errno
from tqdm import tqdm
import argparse
# import textwrap
# import pdb

import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.axes_grid1 import AxesGrid
from PIL import Image

import tensorflow as tf
import inceptionv3
import utils

def prepareTensorflowModel():
    sess = tf.Session()
    x = tf.placeholder(tf.float32, (299, 299, 3))
    x_expanded = tf.expand_dims(x, axis=0)
    logits, preds = inceptionv3.model(sess, x_expanded)
    probs = tf.nn.softmax(logits)
    return sess, x, probs

sess, x, probs = prepareTensorflowModel()

def applyModel299(file_path):
    img = utils.load_image(file_path)
    p = sess.run(probs, feed_dict={x: img})[0]
    pil_img = Image.open(file_path)
    # pdb.set_trace()
    return pil_img, p

def classifyImage(path_input):
  input_image, prediction = applyModel299(path_input)
  return input_image, prediction

def drawImage(input_image, prediction):
  plt.subplot2grid((3,1), (0,0), rowspan=2)

  # Now print out the image and the probability
  plt.imshow(input_image)
  pylab.xticks([])
  pylab.yticks([])

def getPredictions(prediction, lines, ground_truth):

  probabilities = []
  i = 0

  for line in lines:
    line = line.strip('\n')

    words = line.split(' ', 1)
    # cat_id = words[0]
    cat_desc = words[1].split(',', 1)[0]
    cat_desc_list = cat_desc.split(' ')
    # use first and last word combine
    if len(cat_desc_list) == 1:
        cat_desc_short = cat_desc_list[0]
    else:
        cat_desc_short = cat_desc_list[0] + ' ' + cat_desc_list[-1]

    # Only probability followed by description of category
    probabilities.append( ( prediction[i], cat_desc_short ) )
    i = i + 1

  sorted_probabilities = sorted(probabilities, key=lambda tup: tup[0], reverse=True)

  val = []
  labels = []
  for index in range(0, 5):

    val.append( sorted_probabilities[4-index][0] )
    labels.append( sorted_probabilities[4-index][1] )

  val.append(1.0)
  labels.append(ground_truth)
  #
  return (val[:6], labels[:6])


def drawPredictions(values, labels, wrong_label=None):
  ax = plt.subplot2grid((3,1), (2,0))
  ax.margins(y=0)
  pos = pylab.arange(6)    # the bar centers on the y axis

  rects = pylab.barh(pos, values, height=1, alpha=1, edgecolor = "grey")
  ax.set_xlim([0,1])

  ax.set_xticklabels([])

  pylab.yticks([])
  ax.get_xaxis().set_visible(False)

  # Lastly, write in the ranking inside each bar to aid in interpretation
  for rid, rect in enumerate(rects):

    align = 'right'
    xloc = 0.98
    clr = 'black'

    # TODO change the color to shallow blue, rect.set_color("?")
    # add TARGET, if label equals certain name, gives pink color
    if wrong_label and wrong_label == labels[rid]:
        rect.set_color('pink')
    else:
        rect.set_alpha(0.6)

    # w = labels[rid].split(",")
    # shorten_label = w[0]
    # wrapped_label = '\n'.join(textwrap.wrap(shorten_label, 25)) 

    # Center the text vertically in the bar
    yloc = rect.get_y()+rect.get_height()/2.0

    # top label fix
    if (rid == 5):
      rect.set_color("white")
      rect.set_edgecolor("black")
      xloc = 0.5
      align = 'center'

    # No stroke
    # pylab.text(xloc, yloc, wrapped_label, horizontalalignment=align,
    pylab.text(xloc, yloc, labels[rid], horizontalalignment=align,
        verticalalignment='center', color=clr, weight='heavy', size='14')


def generatePlot(input_dir, file_name, output_dir, lines, ground_truth, wrong_label=None):
  # pdb.set_trace()
  path_input = input_dir + "/" + file_name  # Image to classify
  path_save_file = output_dir + "/" + file_name

  image, prediction = classifyImage(path_input)

  fig = plt.figure(figsize=(4.5, 7.5),facecolor='w')

  AxesGrid(fig, 111, # similar to subplot(141)
      nrows_ncols = (2, 1),
      axes_pad = 0.0,
      label_mode = "1",
    )

  values, labels = getPredictions(prediction, lines, ground_truth)

  # print labels
  drawPredictions(values, labels, wrong_label)

  drawImage(image, prediction)

  fig.subplots_adjust(left=0.01, bottom=0.501, top=0.95, right=0.5, wspace = 0.05, hspace = 0.05)

  # Save as image instead of pop-up
  plt.savefig(path_save_file, bbox_inches='tight', dpi=350, pad_inches=0)
  plt.close()
  # print "Saved to file: ", path_save_file

  return None

if __name__ == '__main__':

  ########## start options process

  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input_dir', type=str, default="/Users/cwang/projects/sparse_representation/example/input")
  parser.add_argument('-o', '--output_dir', type=str, default="/Users/cwang/projects/sparse_representation/example/output")
  parser.add_argument('-s', '--synset_dir', type=str, default="/Users/cwang/projects/sparse_representation/example")
  parser.add_argument('-n', '--ignore_prefix', type=int, default=1)
  parser.add_argument('-t', '--wrong_label', type=str, default='guacamole')
  args = parser.parse_args()

  input_dir = os.path.abspath(args.input_dir)

  if args.output_dir is None:
    output_dir = input_dir + '_scores'

    try:
      os.mkdir(output_dir)
    except OSError as exc:
      if exc.errno == errno.EEXIST and os.path.isdir(output_dir):
        pass
      else:
        raise

    print("Saved in the folder: "+output_dir)
  else:
    output_dir = args.output_dir

  ########## End options process

  with open(args.synset_dir + "/" + "synset_words.txt",'r') as f:
    lines = f.readlines() # will append in the list out

  print("data:"+input_dir)
  file_list = []
  for each in os.listdir(input_dir):
    if args.ignore_prefix:
      file_list.append(each)
    elif each.startswith("_tmp_") or each.startswith("ref_"):
      file_list.append(each)
  file_list.sort()

  number = len(file_list)
  for i in tqdm(range(number)):
      if args.ignore_prefix:
        generatePlot(input_dir, file_list[i], output_dir, lines, file_list[i], args.wrong_label)
      else:
        generatePlot(input_dir, file_list[i], output_dir, lines, file_list[i][5:])

