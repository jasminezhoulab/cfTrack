#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -j y
#$ -m a
#$ -l  h_data=5G,h_rt=24:00:00,h_vmem=20G,highp
#$ -t 1-1:1

. /u/local/Modules/default/init/modules.sh

window=3

# script source path
source_path=scripts

# input parameter
input_list=demo/input_list.calculate_IVAF_true_marker.txt

# prerequisites
python=/u/local/apps/anaconda/python2-4.2.0/bin/python
java=/u/local/apps/java/jdk1.8.0_111/bin/java
picard=/u/home/s/shuoli/code/picard/picard.jar
samtools=/u/local/apps/samtools/1.9/bin/samtools
bedtools=/u/local/apps/bedtools/2.29.2/gcc-4.9.3/bin/bedtools
module load samtools
module load bedtools
module load gcc/7.2.0
bedtools=bedtools

read path bed unmerge_plasma_bam name overlap_model nonoverlap_model reference reference_dict <<< "`head -$SGE_TASK_ID ${input_list} | tail -1`"


if [ ! -d "${path}" ]; then
        mkdir -p ${path}
fi


pathname=${path}/${name}
### EXTRACT READS AT BED FILE LOCATIONS  ==> TO OUTPUT_DIR

${java} -Xmx12g -jar ${picard} BedToIntervalList I=${bed} O=${pathname}.interval_list SD=${reference_dict}
${java} -Xmx12g -jar ${picard} FilterSamReads I=${unmerge_plasma_bam} O=${pathname}.paired-reads.bam INTERVAL_LIST=${pathname}.interval_list FILTER=includePairedIntervals SORT_ORDER=coordinate

${samtools} sort -n -o ${pathname}.paired-reads.qsort.bam ${pathname}.paired-reads.bam
${samtools} view ${pathname}.paired-reads.qsort.bam > ${pathname}.paired-reads.qsort.sam
wc -l ${pathname}.paired-reads.qsort.sam > ${pathname}.total_extracted_read_count

### PREPARE BED FILE WITH REFERENCE INFORMATION 

${python} ${source_path}/py6.machinelearn.bed_for_getfasta.py ${window} ${bed} ${pathname}.getfastabed
${bedtools} getfasta -bedOut -fi ${reference} -bed ${pathname}.getfastabed > ${pathname}.fastabed
${python} ${source_path}/py7.machinelearn.bed_for_feature.py ${window} ${pathname}.fastabed ${pathname}.preparebed

### EXTRACT FEATURES FROM READS

${python} ${source_path}/py8.machinelearn.extract_features_from_reads_filter_cluster.with_readname.py ${pathname}.preparebed ${pathname}.paired-reads.qsort.sam ${pathname}.paired-reads.qsort.features ${pathname}.filter_cluster.bed
python ${source_path}/py9.machinelearn.split_overlap_and_nonoverlap.with_readname.py ${pathname}.paired-reads.qsort.features ${pathname}.paired-reads.qsort.overlap.features ${pathname}.paired-reads.qsort.nonoverlap.features
${python} ${source_path}/py10.machinelearn.expand_features_nonoverlap.py query ${pathname}.paired-reads.qsort.nonoverlap.features
python ${source_path}/py10.machinelearn.expand_features_overlap.py query ${pathname}.paired-reads.qsort.overlap.features
 
### CLASSIFY READS

${python} ${source_path}/py11.machinelearn.RandomForest.py ${path} ${pathname}.paired-reads.qsort.overlap.features.expand ${pathname}.paired-reads.qsort.nonoverlap.features.expand  ${overlap_model} ${nonoverlap_model}

${python} ${source_path}/py12.merge_output.add_readname.new_primary_IVAF.py ${pathname}.paired-reads.qsort.overlap.features.expand ${pathname}.paired-reads.qsort.nonoverlap.features.expand ${pathname}.paired-reads.qsort.overlap.features.expand.RFpred.csv ${pathname}.paired-reads.qsort.nonoverlap.features.expand.RFpred.csv ${pathname}.paired-reads.qsort.overlap.features ${pathname}.paired-reads.qsort.nonoverlap.features ${pathname}.overlap.merged_output ${pathname}.nonoverlap.merged_output


rm ${pathname}.interval_list ${pathname}.paired-reads.bam ${pathname}.paired-reads.qsort.bam  ${pathname}.paired-reads.qsort.sam 
rm ${pathname}.getfastabed ${pathname}.fastabed ${pathname}.preparebed ${pathname}.paired-reads.qsort.features ${pathname}.filter_cluster.bed
rm  ${pathname}.paired-reads.qsort.overlap.features ${pathname}.paired-reads.qsort.nonoverlap.features 
rm ${pathname}.paired-reads.qsort.overlap.features.expand ${pathname}.paired-reads.qsort.nonoverlap.features.expand
rm ${pathname}*.var.txt
rm ${pathname}.paired-reads.qsort.overlap.features.expand.RFpred.csv ${pathname}.paired-reads.qsort.nonoverlap.features.expand.RFpred.csv


