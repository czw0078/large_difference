import numpy as np
import imageio
import subprocess

def primitive_defend(x_0_to_1, n_triangle=200, type_primitive='1', tmp_index=1, tmp_dir="./ram"):
    '''
    take in single image or batch of image in numpy array, 
    return reconstructed images as w, h, c array.
    type_shape = '1' is the triangle. 
    '''
    x = x_0_to_1*255
    str_n_triganle = str(n_triangle)
    if len(x.shape) == 4 and x.shape[0] == None:
        x = x[:,:,:]

    # save images in the directory
    str_size = str(x.shape[0])

    input_image_filename=tmp_dir+"/input_"+"{0:05d}".format(tmp_index)+".png"
    output_image_filename=tmp_dir+"/output_"+"{0:05d}".format(tmp_index)+".png"
    print('processing %s' % (input_image_filename))

    # write into full path
    frame = np.uint8(x)
    imageio.imwrite(input_image_filename,frame)

    # call program primitive in shell
    subprocess.call(
       '~/go/bin/primitive -i '+input_image_filename+' -o '+
        output_image_filename+' -n '+str_n_triganle+
        ' -s '+str_size+' -m '+ type_primitive, shell=True)

    # collect results
    y=imageio.imread(output_image_filename)

    return np.array(y)/255.0
