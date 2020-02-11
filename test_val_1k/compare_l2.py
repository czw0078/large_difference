#!/Users/cwang/opt/anaconda3/bin/python
import sys
import numpy as np
from PIL import Image
files = sys.argv[1:]
results = []
for each in files:
    basename = each.split("/")[-1]
    img1=Image.open("resize/"+basename)
    img2=Image.open(each)
    a1 = np.array(img1)
    if len(a1.shape) == 2:
        a1 = np.stack((a1,a1,a1),axis=-1)
    a2 = np.array(img2)
    rmse = np.sum((a1-a2)**2)**0.5
    results.append(rmse)
    print(rmse)
print("average l2 distortion of "+files[0]+" etc.")
print(sum(results)/len(results))

