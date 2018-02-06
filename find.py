import re

N = 118
proxList = list()
distList = list()
proxPosList = list()
distPosList = list()

for i in range(1, N+1, 1):
    proxFlag = True
    distFlag = True
    proxPosFlag = True
    distPosFlag = True

    if i<10:
        name = 'n0' + str(i) + '.hoc'
    else:
        name = 'n' + str(i) + '.hoc'
    with open(name, 'rt') as in_file:
        print('#################')
        for line in in_file:

            if line.find("ProximalSynapses .append(")==0:
                print(line)
                proxFlag = False
                proxList.append(re.sub('[,]',' ',line[25:line.find(")")]))

            if line.find("DistalSynapses .append(")==0:
                print(line)
                distFlag = False
                distList.append(re.sub('[,]',' ',line[23:line.find(")")]))

            if line.find("DistalSynapsePositions .append(")==0:
                print(line)
                distPosFlag = False
                distPosList.append(re.sub('[,]',' ',line[31:line.find(")")]))

            if line.find("ProximalSynapsePositions .append(")==0:
                print(line)
                proxPosFlag = False
                proxPosList.append(re.sub('[,]',' ',line[33:line.find(")")]))


    if proxFlag:
        proxList.append('-1')
    if distFlag:
        distList.append('-1')
    if distPosFlag:
        distPosList.append('-1')
    if proxPosFlag:
        proxPosList.append('-1')

# result = list()
# for line in synList:
#     result.append(list(map(int, line)))
#
with open('proxSyn.dat', 'w') as f:
    for line in proxList:
        f.write(line+'\n')

with open('distSyn.dat', 'w') as f:
    for line in distList:
        f.write(line+'\n')

with open('distPosSyn.dat', 'w') as f:
    for line in distPosList:
        f.write(line+'\n')

with open('proxPosSyn.dat', 'w') as f:
    for line in proxPosList:
        f.write(line+'\n')
