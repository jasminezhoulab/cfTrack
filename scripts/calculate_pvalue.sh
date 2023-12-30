#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -j y
#$ -m a
#$ -l h_data=2G,h_rt=02:00:00,h_vmem=16G
#$ -t 1-1:1

. /u/local/Modules/default/init/modules.sh


module load java/1.7.0_45

# script source path
source_path=scripts

# input parameter
input_list=demo/input_list.calculate_pvalue.txt

# prerequisites
python=/u/local/apps/anaconda/python2-4.2.0/bin/python


read BQ MQ output sampleid trueprefix randomprefix truepath randompath <<< "`head -$SGE_TASK_ID ${input_list} | tail -1`"

${python} ${source_path}/py.calculate_pvalue.py ${BQ} ${MQ} ${output} ${sampleid} ${trueprefix} ${randomprefix} ${truepath} ${randompath}

#rm -rf ${path}


