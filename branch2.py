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
name_b = 'BC'
name_c = 'GC'

# Create cell list
cellsList = list()
cellsList2 = list()

# Create labels for each neuron template
labels = [str(i) for i in range(0, 20, 1)]

# Arange them in a circle
coords = location(20, 1000)
coords2 = location(4, 1700)

# # Feed the cell list
for i in range(0, 20, 1):
    cellsList.append({  'cellLabel': 'GC'+str(i),
                        'x':coords[i][0],
                        'y':coords[i][1],
                    })
for i in range(0, 4, 1):
    cellsList2.append({  'cellLabel': 'BC'+str(i),
                        'x':coords2[i][0],
                        'y':coords2[i][1],
                    })

# Create the population with the cell list
netParams.popParams['popGC'] = {'cellType': 'GC',
                                'cellModel': 'HH',
                                'cellsList': cellsList,
                                'numCells': 1
                                }
for i in range(4):
    netParams.popParams['popBC'+str(i)] = {'cellType': 'BC',
                                    'cellModel': 'HH',
                                    'cellsList': [cellsList2[i],],
                                    'numCells': 1
                                    }



# Import the cells
for i in range(0, 20, 1):
    netParams.importCellParams( label='GC_'+str(i),
                                conds={'cellLabel': 'GC'+str(i)},
                                fileName='BC.hoc',
                                cellName='BasketCell',
                                importSynMechs=True
                                )

# Import the cells
for i in range(0, 4, 1):
    netParams.importCellParams( label='BC_'+str(i),
                                conds={'cellLabel': 'BC'+str(i)},
	                            fileName='BC.hoc',
                                cellName='BasketCell',
                                importSynMechs=True
                                )

# Connection from outer ring to inner ring
limits = [  [[100, 1500],   [-1500, 1500]],
            [[-1500, 1500], [100, 1500]]
        ]
for i in range(2):
    netParams.connParams['BC'+str(i)+'->GC'] = {
                                    'preConds':{'pop':'popBC'+str(i)},
                                    'postConds':{'pop':'popGC',
                                                'x': limits[i][0],
                                                'y': limits[i][1]
                                                },
                                    'sec': 'adend',
                                    'divergence': 5,
                                    'synMech': 'Exp2Syn_0'
                                    }




# Simulation options
simConfig = specs.SimConfig()					# object of class SimConfig to store simulation configuration
simConfig.duration = 1*1e1 			# Duration of the simulation, in ms
simConfig.dt = 0.025 				# Internal integration timestep to use
simConfig.verbose = 0			# Show detailed messages
simConfig.analysis['plotShape'] = {}
simConfig.analysis['plot2Dnet'] = {}
# Create network and run simulation
sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)
#sim.analysis.plotShape()
import pylab; pylab.show()  # this line is only necessary in certain systems where figures appear empty
