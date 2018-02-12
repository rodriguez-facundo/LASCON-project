import numpy as np

from netpyne import specs
from netpyne import sim

from cfg import cfg


# EXTRA FUNCTIONS---------------------------------------------------------------

# IMPORT SECTIONS AND LOCATIONS FOR GRANULE CELLS FROM FILES
# this files contain the indices of each morphological detailed
# granule cell dendrite section, divided in two groups: proximal dendrites and
# distal dendrites. It will be used later to select target sections.

def importSections():
    files = ['morpho/pDend.dat', 'morpho/pPosDend.dat',
             'morpho/dDend.dat', 'morpho/dPosDend.dat']

    # dendrite list where to store the data from files
    dendList = [list() for i in range(4)]

    # for each file
    for i, name in enumerate(files):
        # open the file
        with open(name, 'rt') as in_file:
            # read each line of the file
            for line in in_file:
                # split the string into a list (separated by whitespaces)
                aux = line.split(' ')
                # remove the EOL character at the end
                aux[-1] = aux[-1][:-1]
                # append the list
                dendList[i].append(aux)

    # for each dendrite list
    for (i, dends), v_type in zip(enumerate(dendList), ['int16', 'float']*2):
        # for each list within each dendrite list
        for j, dend in enumerate(dends):
            # convert from string to corresponding type (int or float)
            dendList[i][j] = np.array(dend, dtype=v_type).tolist()

    return dendList

# returns pairs of pre-post synaptic cells indices
# to define connectivity base on list.
def ringConnList(nPre, nPost, conv=1, div=1, span=[0, 1], avoid=False):
    ''' returns a list of connections from pre-synaptic cell population
        to post-synaptic cell population.

        ATENTION:   - each pre-synaptic cell connects only
                      once to the same post-synaptic cell.

    Parameters
    ----------
        nPre : int (default = 1)
            Number of pre-synaptic cells.

        nPost : int (default = 1)
            Number of post-synaptic cells.

        conv : int (default = 1)
            Maximum allowed number of connections
            per post-synaptic cell.

        div : int( default = 1)
            Number of connections per pre-synaptic cell.

        span : list (size(1, 2), default = [0, 1])
            Target range of post-synaptic cells.

        avoid : bool (default = True)
            If True, it avoids self connection.

    Return
    ------
        out : list (shape(nPre*div, 2))
            List of list with pairs of pre and post cells id to be connected
    '''
    from numpy import random

    # check if enough slots available
    if div>span[1]-span[0]:
        raise Exception('Not enough free post-synaptic targets. ' +
                        'Reduce divergency or increase span...')

    # output list
    out = list()

    # counter for post-synaptic convergency
    count = np.zeros(nPost)

    # ratio pre/post synaptic population number
    ratio = 1. * nPre / nPost

    # for each pre-synaptic connection
    for i in range(nPre):
        # create target indices (use mod sum and keep convergency low)
        targets = [(int(i/ratio)+j)%nPost for j in range(span[0], span[1])
                                    if count[(int(i/ratio)+j)%nPost]<conv]

        # avoid self connections
        if avoid and count[i]<conv: targets.remove(i)

        # choose between available post-synaptic indices
        choice = np.random.choice(targets, size=div, replace=False)

        # count chosen post-synaptic cell
        count[choice] +=1

        # append indices to result list
        out += [[i, j] for j in choice ]

    return out


# returns x, y, and z coordinates of points to
# distribute cells in a ring structure
def location(n, r, rot=0):
    '''Returns "n" 3d positions aranged in a circle of radius "r"

    Parameters
    ----------
        n : int
            Number of points
        r : float
            Radius of the circle
        rot: float
            Turns all points by "rot" degrees.

    Returns
    -------
        out : array(n, 3)
            Return numpy array with the x,y,z coordinates
    '''
    def coord(angle):
        return [np.cos(angle), np.sin(angle), 0.]

    points = np.linspace(0, 2*np.pi, n+1)[:-1] + rot *np.pi/180

    return r * np.array([coord(o) for o in points])


# END OF FUNCTION CREATION------------------------------------------------------

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# BEGINNING OF CODE
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# DEFINITIONS

# Network parameters Object Class
netParams = specs.NetParams()

# number of different cell types
cellTypes = 4

# list of cell Labels
labels = ['BC', 'MC', 'HIPP', 'GC']

# name of templates in hoc file
template = ['BasketCell', 'MossyCell', 'HIPPCell', 'GranuleCell']

# topology file name
top_file = 'morpho/Sample_50A50Y.dat'

# number of Granule cells reached by Perforant Path (PP)
nP = 100  # real number is 100

# list containing number of cells for Basket, Mossy and HIPP cells
n = [6, 15, 6, 500]

# list containing diameters of circles for each cell class
r = [500, 1000, 1500, 2000]

# Rotation for the circles (just to impove visualization)
rotation = [30, 0, 0, 0]

# THE FOLLOWING DEFINITIONS ARE BASE ON MATRIX NOTATION FOR CONNECTIVITY
# it reads as:
#               row-> pre-synaptic cell population
#               column-> post-synaptic cell population

# The following values were obtained from:
# ---------------------------------------
# "Combined role of seizure-induced dendritic morphology alterations and spine
# loss in newborn granule cells with mossy fiber sprouting on the
# hyperexcitability of a computer model of the dentate gyrus."
#                           - Tejada J., Garcia-Cairasco N., Roque AC. - 2014
#                           - DOI: 10.1371/journal.pcbi.1003601

# check if the connection is valid
valid = [[True, True, False, True],
         [True, True, True, True],
         [True, True, False, True],
         [True, True, True, False]
         ]

# divergency matrix
diver = [   [2, 5, 0, 100],
            [1, 3, 2, 100],
            [4, 4, 0, 160],
            [2, 1, 3, 10]
        ]

# span from pre-synaptic cells to post-synaptic cells
span =  [[[0, 6],  [0, 15],  False,      [0, 500] ],
         [[0, 6],  [-3, 4],  [-2, 3],    [25, 175]],
         [[0, 6],  [0, 15],  False,      [0, 500] ],
         [[-1, 2], [0, 3],   [-2, 3],    [-50, 51]]
        ]

# convergency
conver = [  [3,     3,  0,      2],
            [4,     4,  6,      7],
            [5,     2,  0,      7],
            [180,   38, 270,    14]
        ]

# matrix of target sections for Mossy, Basket y HIPP cells
sections = [ [['bcdend1_1', 'bcdend2_1'],   'soma',     False  ],
             [['bcdend1_1', 'bcdend2_1'],   'adend',    'bdend'],
             [['bcdend1_3', 'bcdend2_3'],   'cdend',    False  ],
             ['adend',                      'adend',    'adend']
            ]

# weights & delays
synParams = [[  [7.6e-3, .8],   [1.5e-3, 1.5],  False,          [1.6e-3, .85] ],
             [  [0.3e-3, 3],    [0.5e-3, 2],    [0.2e-3, 3],    [0.3e-3, 3]   ],
             [  [0.5e-3, 1.6],  [1.5e-3, 1],    False,          [0.5e-3, 1.6] ],
             [  [4.7e-3, .8],   [0.2e-3, 1.5],  [0.5e-3, 1.5],  [2e-3, 0.8]   ]
            ]


# synaptic mechanisms
#BC inputs
netParams.synMechParams['BC_PP'] = {'mod': 'Exp2Syn', 'tau1': 2, 'tau2': 6.3, 'e': 0}
netParams.synMechParams['BC_GC'] = {'mod': 'Exp2Syn', 'tau1': 0.3, 'tau2': 0.6, 'e': 0}
netParams.synMechParams['BC_MC'] = {'mod': 'Exp2Syn', 'tau1': 0.9, 'tau2': 3.6, 'e': 0}
netParams.synMechParams['BC_BC'] = {'mod': 'Exp2Syn', 'tau1': 0.16, 'tau2': 1.8, 'e': -70}
netParams.synMechParams['BC_HIPP'] = {'mod': 'Exp2Syn', 'tau1': 0.4, 'tau2': 5.8, 'e': -70}

#MC inputs
netParams.synMechParams['MC_PP'] = {'mod': 'Exp2Syn', 'tau1': 1.5, 'tau2': 5.5, 'e': 0}
netParams.synMechParams['MC_GC'] = {'mod': 'Exp2Syn', 'tau1': 0.5, 'tau2': 6.2, 'e': 0}
netParams.synMechParams['MC_MC'] = {'mod': 'Exp2Syn', 'tau1': 0.45, 'tau2': 2.2, 'e': 0}
netParams.synMechParams['MC_BC'] = {'mod': 'Exp2Syn', 'tau1': 0.3, 'tau2': 3.3, 'e': -70}
netParams.synMechParams['MC_HIPP'] = {'mod': 'Exp2Syn', 'tau1': 0.5, 'tau2': 6, 'e': -70}

#HC inputs
netParams.synMechParams['HIPP_GC'] = {'mod': 'Exp2Syn', 'tau1': 0.3, 'tau2': 0.6, 'e': 0}
netParams.synMechParams['HIPP_MC'] = {'mod': 'Exp2Syn', 'tau1': 0.9, 'tau2': 3.6, 'e': 0}
netParams.synMechParams['HIPP_BC'] = {'mod': 'Exp2Syn', 'tau1': 0.4, 'tau2': 5.8, 'e': -70}

#GC inputs
netParams.synMechParams['GC_PP'] = {'mod': 'Exp2Syn', 'tau1': 1.5, 'tau2': 5.5, 'e': 0}
netParams.synMechParams['GC_GC'] = {'mod': 'Exp2Syn', 'tau1': 1.5, 'tau2': 5.5, 'e': 0}
netParams.synMechParams['GC_MC'] = {'mod': 'Exp2Syn', 'tau1': 1.5, 'tau2': 5.5, 'e': 0}
netParams.synMechParams['GC_BC'] = {'mod': 'Exp2Syn', 'tau1': 0.26, 'tau2': 5.5, 'e': -70}
netParams.synMechParams['GC_HIPP'] = {'mod': 'Exp2Syn', 'tau1': 0.5, 'tau2': 6, 'e': -70}

# PERFORANT PATH PP
netParams.stimSourceParams['PP'] = {'type': 'NetStim',
                                    'interval': 100,
                                    'number': 1,
                                    'start': 5,
                                    'noise':0.002
                                    }

# ------------------------------------------------------------------------------

# MAIN CODE

# get coordinates to arange cell populations into cicles
coords = [location(n=n[i], r=r[i], rot=rotation[i]) for i in  range(cellTypes)]

# import topology for Granule cells
topo = np.loadtxt(fname=top_file, dtype='int16')

# import Target sections for morphological detailed Granule cells
secAndLoc = importSections()

# create list of cells location for each population
cellList = [list() for i in range(cellTypes)]

# Feed the list
for i, label in enumerate(labels[:-1]):
    for index in range(n[i]):
        cellList[i].append({'cellLabel': label+str(index),
                            'x':coords[i][index][0],
                            'y':coords[i][index][1]
                            })

# -------------------------CREATE POPULATION------------------------------------
# population of Granule Cells
for i in range(n[-1]):
    netParams.popParams[labels[-1]+str(i)] = {
                            'cellType': labels[-1]+str(i),
                            'cellModel': 'HH',
                            'xRange' : [coords[3][i][0]-1, coords[3][i][0]+1],
                            'yRange' : [coords[3][i][1]-1, coords[3][i][1]+1],
                            'numCells': 1
                         }

# population of BC, MC and HIPP
for index, label in enumerate(labels[:-1]):
    netParams.popParams[label] = {'cellType': label,
                                    'cellModel': 'HH',
                                    'cellsList': cellList[index],
                                    'numCells': 1
                                  }

# IMPORT CELLS
# import Granule cells
for i in range(n[-1]):
    netParams.importCellParams( label=labels[-1]+str(i),
                                conds={'cellType': labels[-1]+str(i) },
                                fileName='templates/n'+str(topo[i])+'.hoc',
                                cellName=template[3]+str(topo[i]),
                                importSynMechs=False
                                )

# import Basket, Mossy and HIPP cells
for index, label in enumerate(labels[:-1]):
    for i in range(n[index]):
        netParams.importCellParams( label=label+str(i),
                                    conds={'cellLabel': label+str(i) },
                                    fileName='templates/'+label+'.hoc',
                                    cellName=template[index],
                                    importSynMechs=False
                                    )

#..........................CONNECT NETWORK--------------------------------------

#connect Basket, Mossy and HIPP cells (Granule excluded)
for pre, preL in enumerate(labels[:-1]):
    for post, postL in enumerate(labels[:-1]):
        if valid[pre][post]:
            targetList = ringConnList(  nPre=n[pre], nPost=n[post],
                                        conv=conver[pre][post],
                                        div=diver[pre][post],
                                        span=span[pre][post],
                                        avoid=True if pre==post else False
                                        )

            netParams.connParams[preL+'_'+postL] = {
                                        'preConds'  : {'pop':preL},
                                        'postConds' : {'pop': postL},
                                        'sec': sections[pre][post],
                                        'synMech'   : postL+'_'+preL,
                                        'weight': synParams[pre][post][0],
                                        'delay': synParams[pre][post][1],
                                        'connList'  : targetList,
                                        'connFunc'  : 'fromListConn'
                                        }

# connect Granule cells to other cells
for post, postL in enumerate(labels[:-1]):
    if valid[3][post]:
        targetList = ringConnList(  nPre=n[-1], nPost=n[post],
                                    conv=conver[3][post], div=diver[3][post],
                                    span=span[3][post]
                                    )

        targetList = [[0, v] for u, v in targetList]
        for preid in range(n[-1]):
            div = diver[3][post]
            subTargetList = targetList[preid*div:(preid+1)*div]
            netParams.connParams['GC'+str(preid)+'_'+postL] = {
                                'preConds'  : {'pop':'GC'+str(preid)},
                                'postConds' : {'pop': postL},
                                'sec': sections[3][post],
                                'synMech'   : postL+'_GC',
                                'weight':synParams[3][post][0],
                                'delay':synParams[3][post][1],
                                'connList'  : subTargetList,
                                'connFunc'  : 'fromListConn'
                                }

# connect Mossy, Basket and HIPP cells to Granule cells
for cellId, preL in enumerate(labels[:-1]):
    # target sections on granule cells could be distal dentrites, proximal
    # dendrites or soma depending on pre-synaptic cell population
    k = 0
    flag = False
    if preL=='MC':
        flag = True
        zone = 0
    elif preL=='HIPP':
        flag=True
        zone=2

    targetList = ringConnList(  nPre=n[cellId], nPost=n[-1],
                                conv=conver[cellId][3], div=diver[cellId][3],
                                span=span[cellId][3]
                                )

    # mossy cells connects twice to Granule cells: ones to (-175,-25) range
    # and again to (25,175) range.
    if preL=='MC': targetList += ringConnList(nPre=n[cellId], nPost=n[-1],
                                conv=conver[cellId][3], div=diver[cellId][3],
                                span=[-span[cellId][3][1], -span[cellId][3][0]]
                                )

    for preid, postid in targetList:
        # if pre-synatic cells are Mossy or HIPP cells, connect to dendrites
        if flag:
            target = [ 'dend_'+str(j) for j in secAndLoc[zone][topo[postid]-1]]
        # if pre-synaptic cells are Basket cells, connect to soma
        else:
            # check if netpyne imported soma defined as: "soma" or "soma_0"
            keyList = netParams.cellParams['GC'+str(postid)]['secs'].keys()
            if 'soma' in keyList:
                target = 'soma'
            elif 'soma_0' in keyList:
                target = 'soma_0'
            else:
                print('No soma found')

        # create connection dictionary
        netParams.connParams[preL+'_'+'GC'+str(k)] = {
                                'preConds'  : {'pop': preL},
                                'postConds' : {'cellType': 'GC'+str(postid)},
                                'synMech'   : 'GC_'+preL,
                                'sec': target,
                                'weight': synParams[cellId][3][0],
                                'delay': synParams[cellId][3][1],
                                'connList'  : [[preid, 0],],
                                'connFunc'  : 'fromListConn'
                                }
        k +=1


# Connect from Granule cell to Granule cells
targetList = ringConnList(  nPre=n[-1], nPost=n[-1], conv=conver[3][3],
                            div=diver[3][3],span=span[3][3], avoid=True
                            )

k = 0
for preid, postid in targetList:
    target = [ 'dend_'+str(i) for i in secAndLoc[0][topo[postid]-1] ]
    netParams.connParams['GG_GC'+str(k)] = {
                            'preConds' : {'cellType': labels[-1]+str(preid)},
                            'postConds': {'cellType': labels[-1]+str(postid)},
                            'synMech'  : 'GC_GC',
                            'sec'      : target,
                            'weight'   : synParams[3][3][0],
                            'delay'    : synParams[3][3][1],
                            }
    k +=1


# --------------------------------STIMULUS--------------------------------------

# Stimulate 100 Granule cells
for i in range(nP):
    syns = len(secAndLoc[2][topo[i]-1])
    secs = ['dend_'+str(sec) for sec in secAndLoc[2][topo[i]-1]]
    # reach all distal dendrites
    netParams.stimTargetParams['PP->GC'+str(i)] = {
                                    'source': 'PP',
                                    'sec':secs,
                                    'loc': 0.5,
                                    'weight': 0.02,
                                    'delay': 3,
                                    'synMech': 'GC_PP',
                                    'conds': {'cellType': labels[-1]+str(i)},
                                    'synsPerConn': syns
                                    }


# Stimulate 1 Mossy cells
netParams.stimTargetParams['PP->MC'] = {
                            'source': 'PP',
                            'sec':'mcdend1_0',
                            'loc': 0.5,
                            'weight': 0.5e-2,
                            'delay': 3,
                            'synMech': 'MC_PP',
                            'conds': {  'pop': 'MC',
                                        'cellList': [1,]}
                            }

# --------------------------------END FILE--------------------------------------
