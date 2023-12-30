
import sys


target_bed = sys.argv[1]
mask_bed = sys.argv[2]
marker_bed = sys.argv[3]
output = sys.argv[4]
path = sys.argv[5]

marker = open(marker_bed, "r")
MAX = 0
for line in marker:
    MAX += 1

marker.close()



loci_dict = {}

f = open(target_bed)
for line in f:
    sp = line.strip().split('\t')
    for i in range(int(sp[1]), int(sp[2]) + 1):
        loci_dict[sp[0] + '\t' + str(i)] = True

f.close()


f = open(mask_bed)
for line in f:
    sp = line.strip().split('\t')
    for i in range(int(sp[1]), int(sp[2]) + 1):
        loci_dict[sp[0] + '\t' + str(i)] = False

f.close()




mutation = []
key = loci_dict.keys()
for i in key:
    if loci_dict[i]:
        mutation.append(i)




import random
for i in range(100):
    for n in [MAX]: #range(50, MAX + 50, 50):
        sampling_mutation = random.sample(mutation, n)
        g = open(path + "/" + output + "_random" + str(n) + "_" + str(i+1) + ".txt", 'w')
        for mut in sampling_mutation:
            sp = mut.split('\t')
            g.write(sp[0] + '\t' + str(int(sp[1])-1) + '\t' + sp[1] + '\n')
        g.close()
    

