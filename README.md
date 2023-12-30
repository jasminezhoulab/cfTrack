# INTRODUCTION
cfTrack is a cfDNA-based cancer monitoring method, that overcomes limitations of previous targeted sequencing methods by analyzing tumor mutations across the whole exome. Taking advantage of the broad genome coverage of WES data, cfTrack can sensitively detects MRD and cancer recurrence by integrating signals across the known clonal tumor mutations of a patient. In addition, cfTrack detects tumor evolution and second primary cancers by de novo identifying emerging tumor mutations using cfSNV. In summary, cfTrack can sensitively and specifically monitor the full spectrum of cancer treatment outcomes using exome-wide mutation analysis. 

cfTrack is licensed under a Creative Commons Attribution-Noncommercial 4.0 International License, and can be obtained at https://zhoulab.dgsom.ucla.edu/pages/cfTrack with registration. cfTrack contains two parts: tumor-informed monitoring and tumor-naive monitoring. The tumor-informed monitoring codes are included in the package. The tumor-naive monitoring utilizes cfSNV, a sensitive SNV detection tool that we previously developed. cfSNV is not included in this package and can be obtained at https://zhoulab.dgsom.ucla.edu/pages/cfSNV. 

# PREREQUISITE PACKAGES
cfTrack was developed on UCLA Hoffman2 cluster. All the analyses in this study were done there. The system information of UCLA Hoffman2 cluster is:
Linux n6015 2.6.32-754.14.2.el6.x86_64 #1 SMP Tue May 14 19:35:42 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
There is no non-standard hardware required.

1) java 1.8.0_111 (Just need to be compatible to picard tools)
2) samtools 1.9: https://sourceforge.net/projects/samtools/files/samtools/
3) picard 2.18.4: https://github.com/broadinstitute/picard/releases/tag/2.18.4
4) bedtools 2.26.0: https://github.com/arq5x/bedtools2/releases/tag/v2.26.0
5) python 2.7.14
6) numpy 1.13.3
7) sklearn 0.19.1

# INSTALLATION
cfTrack algorithm is implemented using python scripts for now. There is no specific installation needed, if all required packages and tools listed in PREREQUISITE PACKAGES are successfully installed. All the source codes (python codes) are saved under scripts folder.

The use of python codes are wrapped using bash scripts (".sh" scripts). These scripts are started with PBS (portable batch system, the job scheduling system on UCLA Hoffman2) configurations. The configuration parameters basically set the resources required to run the bash scripts. If the users' computing environment is under different scheduling system, the user could change the configuration part according to their needs. 

The paths to the required tools are set for UCLA Hoffman2 cluster. To run cfTrack algorithm in other environment, absolute paths to the required tools in PREREQUISITE PACKAGES section in ".sh" scripts need to be changed to where these packages are installed in users' computing environment. 

# USAGE
The cfTrack algorithm is packed using bash scripts (in the folder "scripts/"). In each bash script, the code starts with configuration settings: "input parameter" and "prerequisites".
- "input parameter" is a input table which contains paths to the required input files. Each line in this table is a complete set of required input files for the script. The bash script could be set to run for different lines of inputs in this table in parallel.
- "prerequisites" is a list of absolute paths to required tools.

To run cfTrack, the users could run the bash scripts in the following order:

1. generate_random_marker.sh
  - This bash script basically generates random marker sets for modeling the sample-specific background noise distribution.  The required inputs are shown below:
  - path: full path of output directory.
  - target_bed: full path to bed format file with exome target regions.
  - mask_bed: full path to bed format file with regions that needs to be masked for generating background noise distribution, e.g. indel regions, germline mutations, somatic mutations, clonal hematopoiesis of indeterminate potential.
  - marker_bed: full path to bed format file with pre-existing mutation sites that identified from the pre-treatment samples.
  - output: output prefix
  - This script generates 100 sets of random sampling sites. Each set contains the same number of genomic loci as marker_bed.

2. calculate_IVAF_true_marker.sh 
  - This bash script is to calculate integrated variant allele frequency (IVAF) at the pre-existing mutation sites in the post-treatment sample. The required inputs are shown below:
  - path: full path of output directory.
  - bed: full path to bed format file with pre-existing mutation sites.
  - unmerge_plasma_bam: full path to bam file of the post-treatment sample.
  - name: file prefix for the output.
  - overlap_model: full path to the random forest model for overlapping read mates. Note that the model file in the folder "models/" can be downloaded at https://zhoulab.dgsom.ucla.edu/pages/cfTrack due to its large file size.
  - nonoverlap_model: full path to the random forest model for non-overlapping read mates. Note that the model file in the folder "models/" can be downloaded at https://zhoulab.dgsom.ucla.edu/pages/cfTrack due to its large file size.
  - reference: full path to reference sequence in fasta format.
  - reference_dict: full path to reference sequence dictionary file created from picard tools CreateSequenceDictionary.
  - This script generates three files. "*.total_extracted_read_count" contains the total number of examined reads at the genomic loci in "bed". "*.overlap.merged_output" contains the classification results of the overlapping read mates with variant alleles. "*.nonoverlap.merged_output" contains the classification results of the overlapping read mates with variant alleles. 

3. calculate_IVAF_random_marker.sh
  - This bash script is to calculate integrated variant allele frequency (IVAF) at the random sampling sites (from generate_random_marker.sh) in the post-treatment sample. The required inputs are shown below:
  - path: full path of output directory.
  - bed: full path to bed format file with random sampling sites.
  - unmerge_plasma_bam: full path to bam file of the post-treatment sample.
  - name: file prefix for the output.
  - overlap_model: full path to the random forest model for overlapping read mates.
  - nonoverlap_model: full path to the random forest model for non-overlapping read mates.
  - reference: full path to reference sequence in fasta format.
  - reference_dict: full path to reference sequence dictionary file created from picard tools CreateSequenceDictionary.
  - This script generates three files. "*.total_extracted_read_count" contains the total number of examined reads at the genomic loci in "bed". "*.overlap.merged_output" contains the classification results of the overlapping read mates with variant alleles. "*.nonoverlap.merged_output" contains the classification results of the overlapping read mates with variant alleles. 

4. calculate_pvalue.sh
  - This bash script calculates an empirical p-value for MRD/recurrence. The required inputs are shown below:
  - BQ: minimum base quality (phred score) for a variant read to be considered as high quality
  - MQ: minimum mapping  quality (phred score) for a variant read to be considered as high quality
  - output: full path to output file
  - sampleid: sample id
  - trueprefix: prefix for the count files from the pre-existing mutation sites ("name" in calculate_IVAF_true_marker.sh)
  - randomprefix: prefix for the count files from the random sampling sites ("name" in calculate_IVAF_random_marker.sh)
  - truepath: full path to the count files from the pre-existing mutation sites ("path" in calculate_IVAF_true_marker.sh)
  - randompath: full path to the count files from the random sampling sites ("path" in calculate_IVAF_random_marker.sh))
  - This script generates a single output file, which includes the estimated IVAF at the pre-existing mutation sites and the empirical p-value.

# OUTPUT
There is one output file from cfTrack, which is specified by user in calculate_pvalue.sh as input "output".The file contains two numbers: the estimated IVAF at the pre-existing mutation sites and the empirical p-value.

# DEMO: EXAMPLE DATA
A demo is provided along with the scripts. Example data and required reference files are saved under demo folder ("demo/"). Note that all files in demo folder can be downloaded at https://zhoulab.dgsom.ucla.edu/pages/cfTrack due to their large file sizes.

1) chr22.fa: reference genome (from UCSC genome browser hg19).
2) chr22.fa.*: genome indices created for bwa, samtools, GATK and picard tools.
3) example_output folder: expected output file and intermediate files.
   a) plasma.pvalue.txt: output file with IVAF and p-value.
   b) TEST: a folder contains 100 sets of random sampling genomic sites from "generate_random_marker.sh".
   c) TEST_OUTPUT: a folder contains intermediate count files from "calculate_IVAF_true_marker.sh" and "calculate_IVAF_random_marker.sh".
4) target.bed: targeted regions (e.g. capture regions of WES)
5) plasma.bam and plasma.bai: aligned reads of the post-treatment sample
6) marker.bed: pre-existing mutation sites
7) mask.bed: genomic regions to be masked in "generate_ranodm_marker.sh"
8) input_list.generate_random_marker.txt: "input parameter" for generate_random_marker.sh
   This file contains one line for the demo sample.
9) input_list.calculate_IVAF_true_marker.txt: "input parameter" for calculate_IVAF_true_marker.sh
   This file contains one line for the pre-existing mutation sites.
10) input_list.calculate_IVAF_random_marker.txt: "input parameter" for calculate_IVAF_random_marker.sh
   This file contains 100 line, each for one set of the random sampling sites.
11) input_list.calculate_pvalue.txt: "input parameter" for calculate_pvalue.sh
   This file contains one line for the demo sample.

 This demo was expected to run less than 20min. Please change the paths to "input parameter" and "prerequisites" in each .sh script. Then the algorithm could be run simply through the bash scripts. 

## open the code package and run .sh scripts (in the folder "scripts/") in order
1. generate_random_marker.sh
2. calculate_IVAF_true_marker.sh
3. calculate_IVAF_random_marker.sh
4. calculate_pvalue.sh


