# sparse_representation
Repo of the source code for the paper "Sparse Representation And Adversarial Robustness" 

* [install](https://github.com/fogleman/primitive) the go language and the app "primitive" at ~/go/bin/primitive 
* python 3.7 and tensorflow 1.13 tested
* git clone this repo
* ./setup.sh to download inception_v3 model

This framework use pre-trained model, the author used cpu version of tensorflow and python from Anaconda.

# File Structure:

* pkl stored in test_val_1k/parameter_xxxx/snapshot_xxxx/start_xxxx
controlled by provider

* output stored in results/parameter_xxxx/snapshot_xxxx/start_xxxx
controlled by the .pbs

* primitive tmp files stored in dev/shm/ram/parameter_xxxx
controlled by the .pbs

# Analysis
bash script

```bash
for each in start_*/*out.out; do tail -n 1 $each >> tmp.out; done
cut -f 4 -d ' ' tmp.out
```
