#!/bin/bash
# qsub -v n=0200 reconstruct_template.pbs
# qsub -v n=0400 reconstruct_template.pbs
# qsub -v n=0600 reconstruct_template.pbs
# qsub -v n=0800 reconstruct_template.pbs
# sleep 4
# qsub -v n=1000 reconstruct_template.pbs
# qsub -v n=1200 reconstruct_template.pbs
# qsub -v n=1400 reconstruct_template.pbs
# qsub -v n=1600 reconstruct_template.pbs
# sleep 4
# qsub -v n=1800 reconstruct_template.pbs
qsub -v n=2000 reconstruct_template.pbs
