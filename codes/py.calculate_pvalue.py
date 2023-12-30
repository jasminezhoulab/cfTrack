
import sys
import glob, os


BQ_threshold = int(sys.argv[1])
MQ_threshold = int(sys.argv[2])
score_threshold = 0.5

outputfile = sys.argv[3]
sampleid = sys.argv[4]
trueprefix = sys.argv[5]
randomprefix = sys.argv[6]
truefolder = sys.argv[7]
randomfolder = sys.argv[8]

output = open(outputfile, 'w')

true_count_list = glob.glob(truefolder + "/" + trueprefix + "*.total_extracted_read_count")
random_count_list = glob.glob(randomfolder + "/" + randomprefix + "*.total_extracted_read_count")
count_list = dict([])
for true_count in true_count_list:
	count_list[true_count] = "true"

for random_count in random_count_list:
	count_list[random_count] = "random"

random_IVAF = []
count_file_list = count_list.keys()

for i in range(0,len(count_file_list)):
    count_file = count_file_list[i]
    overlap_file = '.'.join(count_file.split('.')[0:(len(count_file.split('.'))-1)]) + ".overlap.merged_output"
    nonoverlap_file = '.'.join(count_file.split('.')[0:(len(count_file.split('.'))-1)]) + ".nonoverlap.merged_output"
    try:
        fcount = open(count_file)
    except IOError:
        continue
    temp = fcount.readline()
    if temp == "":
        continue
    else:
        count = float(temp.split()[0])
        fcount.close()
    n = 0
    read_id = set([])
    try:
        foverlap = open(overlap_file)
        for line in foverlap:
            sp = line.strip().split('\t')
            if int(sp[1]) > MQ_threshold and int(sp[14]) > BQ_threshold and float(sp[256]) >= score_threshold:
                n += 1
                read_id.add(sp[257])
        foverlap.close()
    except IOError:
        continue
    try:
        fnonoverlap = open(nonoverlap_file)
        for line in fnonoverlap:
            sp = line.strip().split('\t')
            if int(sp[1]) > MQ_threshold and int(sp[14]) > BQ_threshold and float(sp[144]) >= score_threshold:
                n += 1
                read_id.add(sp[145])
        fnonoverlap.close()
    except IOError:
        continue
    if count_list[count_file] == "true":
        true_IVAF = float(len(read_id))/float(count)
    else:
        random_IVAF.append( float(len(read_id))/float(count) )

higher_random_count = sum([1.0 for i in random_IVAF if i > true_IVAF ])
p_value = float(higher_random_count)/float(len(random_IVAF))
output.write("sampleID\tIVAF\tp\n")
output.write(sampleid + "\t" + str(true_IVAF) + "\t" + str(p_value) + "\n")

output.close()





