from netpyne import specs
from netpyne import sim
import numpy as np
from numpy import linspace as ls
import json

def location(n, r):
    '''Returns "n" 3d positions aranged in a circle of radius "r"

    Parameters
    ----------
        n : int
            Number of points
        r : float
            Radius of the circle

    Returns
    -------
        out : array(n, 3)
            Return numpy array with the x,y,z coordinates
    '''
    def coord(angle):
        return [np.cos(angle),np.sin(angle), 0.]

    return r * np.array([coord(theta) for theta in ls(0, 2*np.pi, n+1)[:-1]])
# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

## Population parameters
#netParams.popParams['HH_pop'] = {'cellType': 'PYR', 'numCells': 5, 'cellModel': 'HH'}
#netParams.popParams['HH3D_pop'] = {'cellType': 'PYR2', 'numCells': 1, 'cellModel': 'HH3D'}
# netParams.popParams['Traub_pop'] = {'cellType': 'PYR', 'numCells': 5, 'cellModel': 'Traub'}

# Create a name
name = 'BC'

# Create cell list
cellsList = list()
cellsList2 = list()

# Create labels for each neuron template
labels = [str(i) for i in range(0, 20, 1)]

# Arange them in a circle
coords = location(20, 1000)
coords2 = location(4, 1700)

# Feed the cell list
for i in range(0, 20, 1):
    cellsList.append({  'cellLabel': labels[i],
                        'x':coords[i][0],
                        'y':coords[i][1],
                    })
for i in range(0, 4, 1):
    cellsList2.append({  'cellLabel': labels[i]+'_2',
                        'x':coords2[i][0],
                        'y':coords2[i][1],
                    })

# Create the population with the cell list
netParams.popParams['PYR_HH'] = {'cellType': 'PYR',
                                'cellModel': 'HH',
                                'cellsList': cellsList,
                                'numCells': 1
                                }

netParams.popParams['PYR2_HH'] = {'cellType': 'PYR2',
                                'cellModel': 'HH2',
                                'cellsList': cellsList2,
                                'numCells': 1
                                }



# Import the cells
for i in range(80, 100, 1):
    netParams.importCellParams( label='PYR_HH_rule'+str(i-80),
                                conds={'cellLabel': labels[i-80]},
	                            fileName='BC.hoc',
                                cellName='BasketCell',
                                importSynMechs=True
                                )

# Import the cells
for i in range(0, 4, 1):
    netParams.importCellParams( label='PYR_HH_rule_2'+str(i),
                                conds={'cellLabel': labels[i]+ '_2'},
	                            fileName='BC.hoc',
                                cellName='BasketCell',
                                importSynMechs=True
                                )

#print(json.dumps(netParams.synMechParams, indent=4))
connlist = [[0, 0],[0,2],[0,4],[0,6],[0,8]]

# Connection from outer ring to inner ring
netParams.connParams['O->I'] = {
                                'preConds':{'pop':'PYR2_HH'},
                                'postConds':{'pop':'PYR_HH'},
                                'sec': 'adend',
                                'synMech': 'Exp2Syn_0',
                                'connFunc': 'fromListConn',
                                'connList': connlist,
}




# Simulation options
simConfig = specs.SimConfig()					# object of class SimConfig to store simulation configuration
simConfig.duration = 1*1e1 			# Duration of the simulation, in ms
simConfig.dt = 0.025 				# Internal integration timestep to use
simConfig.verbose = 0			# Show detailed messages
simConfig.analysis['plotShape'] = {'showSyns': True}
simConfig.analysis['plot2Dnet'] = {'saveFig': 'conn_with_connList.png'}
# Create network and run simulation
sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)
#sim.analysis.plotShape()
import pylab; pylab.show()  # this line is only necessary in certain systems where figures appear empty
