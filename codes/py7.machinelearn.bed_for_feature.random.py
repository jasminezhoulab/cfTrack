import sys
W = int(sys.argv[1])
fname = sys.argv[2]
gname = sys.argv[3]
f = open(fname, 'r')
g = open(gname, 'w')
for line in f:
	sp = line.strip().split('\t')
	out = [sp[0], str(int(sp[1])+W), str(int(sp[2])-W), sp[3].upper(), sp[3].upper()[W], 'N']
	g.write('\t'.join(out) + '\n')

g.close()
f.close()



