import sys

foverlap = open(sys.argv[1])
fnonoverlap = open(sys.argv[2])
loverlap = open(sys.argv[3])
lnonoverlap = open(sys.argv[4])

output1 = open(sys.argv[5], 'w')
output2 = open(sys.argv[6], 'w')
line = foverlap.readline()
for line in foverlap:
	output1.write(line.strip() + '\t' + loverlap.readline())

foverlap.close()
loverlap.close()
output1.close()

line = fnonoverlap.readline()
for line in fnonoverlap:
	output2.write(line.strip() + '\t' + lnonoverlap.readline())

fnonoverlap.close()
lnonoverlap.close()
output2.close()

