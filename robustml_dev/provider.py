from abc import ABCMeta, abstractmethod
import os
import glob
import numpy as np
import pickle
import gzip
import PIL.Image

from . import dataset as d

class Provider(metaclass=ABCMeta):
    @abstractmethod
    def provides(self, dataset):
        '''
        Returns whether or not this provider can provide data for the given
        dataset.
        '''
        raise NotImplementedError

    @abstractmethod
    def __len__(self):
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, index):
        '''
        Returns a tuple (x, y) containing the data and label of the given
        index.
        '''
        raise NotImplementedError

class MNIST(Provider):
    def __init__(self, image_path, label_path):
        '''
        image_path is a path to the 't10k-images-idx3-ubyte.gz' from
        'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz'

        label_path is a path to the 't10k-labels-idx1-ubyte.gz' from
        'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'
        '''
        with gzip.open(image_path, 'rb') as f:
            images = f.read()
        assert images[:4] == b'\x00\x00\x08\x03'
        images = np.frombuffer(images[16:], dtype=np.uint8)
        assert len(images) == 7840000
        images = images.reshape((10000, 28, 28)).astype(np.float32) / 255.0
        with gzip.open(label_path, 'rb') as f:
            labels = f.read()
        assert labels[:4] == b'\x00\x00\x08\x01'
        labels = np.frombuffer(labels[8:], dtype=np.uint8)
        assert len(labels) == 10000

        self.xs = images
        self.ys = labels

    def provides(self, dataset):
        return isinstance(dataset, d.MNIST)

    def __len__(self):
        return 10000

    def __getitem__(self, index):
        x = self.xs[index]
        y = self.ys[index]
        # add None for consistency
        return x, y, None

class CIFAR10(Provider):
    def __init__(self, test_data):
        '''
        test_data is a path to the 'test_batch' file from
        'http://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'
        '''
        with open(test_data, 'rb') as f:
            data = pickle.load(f, encoding='bytes')
        self.xs = data[b'data'].reshape((10000,3,32,32)).astype(np.float32) / 255.0
        self.xs = np.transpose(self.xs, (0,2,3,1)) # (N,3,32,32) -> (N,32,32,3)
        self.ys = data[b'labels']

    def provides(self, dataset):
        return isinstance(dataset, d.CIFAR10)

    def __len__(self):
        return 10000

    def __getitem__(self, index):
        # add None for consistence
        return self.xs[index], self.ys[index], None

class ImageNet(Provider):
    def __init__(self, path, shape):
        self._path = path
        self._shape = shape

    def provides(self, dataset):
        return isinstance(dataset, d.ImageNet) and self._shape == dataset.shape

    def __len__(self):
        return 50000

    def __getitem__(self, index):
        data_path = os.path.join(self._path, 'val')
        image_paths = sorted([os.path.join(data_path, i) for i in os.listdir(data_path)])
        assert len(image_paths) == 50000
        labels_path = os.path.join(self._path, 'val.txt')
        with open(labels_path) as labels_file:
            labels = [i.split(' ') for i in labels_file.read().strip().split('\n')]
            labels = {os.path.basename(i[0]): int(i[1]) for i in labels}
        path = image_paths[index]
        x = self._load_image(path)
        y = labels[os.path.basename(path)]
        # return x, y modified to add path
        return x, y, None

    # get centered crop of self._size
    def _load_image(self, path):
        h, w, c = self._shape
        aspect = w / h
        image = PIL.Image.open(path)
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

        arr = np.asarray(image).astype(np.float32) / 255.0
        if arr.ndim == 2:
            # stack greyscale image
            arr = np.repeat(arr[:,:,np.newaxis], repeats=3, axis=2)
        if arr.shape[2] == 4:
            # remove alpha channel
            arr = arr[:,:,:3]
        assert arr.shape == self._shape
        return arr

class ImageNet_val_1k(Provider): # change into ImageNet_val_1k
    def __init__(self, path, shape, tag, start, n_snapshot=-1): # tag for parameter, start for --start option 
        self._path = path
        self._shape = shape
        self._tag = tag 
        self._start = start
        self._snapshot = n_snapshot

    def provides(self, dataset):
        return isinstance(dataset, d.ImageNet) and self._shape == dataset.shape

    def __len__(self):
        return 1000

    def get_image_item(self, index):
        data_path = os.path.join(self._path, 'val')
        image_paths = sorted([os.path.join(data_path, i) for i in os.listdir(data_path)])
        assert len(image_paths) == 1000
        labels_path = os.path.join(self._path, 'val.txt')
        with open(labels_path) as labels_file:
            labels = [i.split(' ') for i in labels_file.read().strip().split('\n')]
            labels = {os.path.basename(i[0]): int(i[1]) for i in labels}
        path = image_paths[index]
        name = path.rsplit('.',1)[0].rsplit('/',2)[-1]
        x = self._load_image(path)
        y = labels[os.path.basename(path)]
        return x, y, name        

    def get_pickle_item(self, pkl_path): 
        x = pickle.load(open(pkl_path, 'rb'))
        return x 

    def __getitem__(self, index):
        x_orig, y, name = self.get_image_item(index)
        # name = ILSVRC2012_val_00049837
        pkl_list = glob.glob(
            self._path+'/parameter_'+self._tag+'/snapshot_*'+'/start_%04d'%(self._start)+'/'+name+'.pkl')
        n_pkl = len(pkl_list)

        # new added: set the snapshot
        if self._snapshot != -1:
            nsp = self._snapshot - 1
            if nsp > 0:
                pkl_path = self._path+'/parameter_'+self._tag+'/snapshot_%04d'%(nsp)+'/start_%04d'%(self._start)+'/'+name+'.pkl'  
                x_adv = self.get_pickle_item(pkl_path)
            else:
                x_adv = np.copy(x_orig)
        else:
            if n_pkl > 0:
                x_adv = self.get_pickle_item(pkl_list[-1])
            else:
                x_adv = np.copy(x_orig)
         
        new_pkl_path = self._path+'/parameter_'+self._tag+'/snapshot_%04d'%(n_pkl+1)+'/start_%04d'%(self._start)+'/'+name+'.pkl'
        return x_adv, x_orig, y, new_pkl_path 

    # get centered crop of self._size
    def _load_image(self, path):
        h, w, c = self._shape
        aspect = w / h
        image = PIL.Image.open(path)
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

        arr = np.asarray(image).astype(np.float32) / 255.0
        if arr.ndim == 2:
            # stack greyscale image
            arr = np.repeat(arr[:,:,np.newaxis], repeats=3, axis=2)
        if arr.shape[2] == 4:
            # remove alpha channel
            arr = arr[:,:,:3]
        assert arr.shape == self._shape
        return arr
