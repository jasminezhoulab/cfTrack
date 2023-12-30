import sys

foverlap = open(sys.argv[1])
fnonoverlap = open(sys.argv[2])
loverlap = open(sys.argv[3])
lnonoverlap = open(sys.argv[4])
rnoverlap = open(sys.argv[5])
rnnonoverlap = open(sys.argv[6])

output1 = open(sys.argv[7], 'w')
output2 = open(sys.argv[8], 'w')
line = foverlap.readline()
for line in foverlap:
	rn = rnoverlap.readline().strip().split('\t')
	rn = rn[len(rn) - 1]
	output1.write(line.strip() + '\t' + loverlap.readline().strip() + '\t' +  rn + '\n')

foverlap.close()
loverlap.close()
output1.close()

line = fnonoverlap.readline()
for line in fnonoverlap:
	rn = rnnonoverlap.readline().strip().split('\t')
	rn = rn[len(rn) - 1]
	output2.write(line.strip() + '\t' + lnonoverlap.readline().strip() + '\t' +  rn + '\n')

fnonoverlap.close()
lnonoverlap.close()
output2.close()

