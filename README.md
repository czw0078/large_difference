# Improving robustness of deep neural network via large-difference transformation
This is the source code repo for the paper "Improving robustness of deep neural network via large-difference transformation" https://www.sciencedirect.com/science/article/pii/S092523122100504X 

# Requirements
* [install](https://github.com/fogleman/primitive) the go language and the app "primitive" at ~/go/bin/primitive 
* python 3.7 and tensorflow 1.13 tested
* git clone this repo
* ./setup.sh to download inception_v3 model

This framework use pre-trained model, the author used cpu version of tensorflow and python from Anaconda.

## Files Overview:

* pkl stored in test_val_1k/parameter_xxxx/snapshot_xxxx/start_xxxx
controlled by provider

* output stored in results/parameter_xxxx/snapshot_xxxx/start_xxxx
controlled by the .pbs

* primitive tmp files stored in dev/shm/ram/parameter_xxxx
controlled by the .pbs

## Running commands
Some useful commands for runing experiments. Due to the large computation resource required for reconstruct the image, we run them on the cluster with job batch runing and schedule system called PBS.

### Check Completeness
```bash
tail -n 1 start_*/*out.out;
```

### Clean And Re-run:
```bash
./submit_multiple_jobs_fix.sh experiment_E_template.pbs 1400 1400 1
qstat -u czw0078
```

### Analysis
bash script

```bash
for each in start_*/*out.out; do tail -n 1 $each >> tmp.out; done
cut -f 4 -d ' ' tmp.out
```
