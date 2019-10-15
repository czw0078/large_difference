import numpy as np
import imageio
import subprocess

def primitive_defend(x_0_to_1, n_triangle=200, cur_dir="./ram"):
    '''
    take in single image or batch of image in numpy array, 
    return reconstructed images as n, w, h, c array.

    '''
    x = x_0_to_1*255
    str_n_triganle = str(n_triangle)
    if len(x.shape) == 4 and x.shape[0] == None:
        x = x[:,:,:]

    if len(x.shape) == 3:
        x = np.expand_dims(x, 0)

    # save images in the directory
    n_image = x.shape[0]
    str_size = str(x.shape[1])
    y = []

    for i in range(n_image):

        input_image_filename=cur_dir+"/input_"+"{0:05d}".format(i)+".png"
        output_image_filename=cur_dir+"/output_"+"{0:05d}".format(i)+".png"
        print('step %d, processing %s' % (i,input_image_filename))

        # write into full path
        frame = np.uint8(x[i])
        imageio.imwrite(input_image_filename,frame)

        # call program primitive in shell
        subprocess.call(
            '~/go/bin/primitive -i '+input_image_filename+' -o '+
            output_image_filename+' -n '+str_n_triganle+
            ' -s '+str_size, shell=True)

        # collect results
        y.append(imageio.imread(output_image_filename))

    return np.array(y)/255.0
