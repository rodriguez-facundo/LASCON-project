import numpy as np
from netpyne import sim
from netpyne import specs

netParams = specs.NetParams()

netParams.popParams['GC1'] = {'cellType': 'GC1',
                                    'cellLabel':'GC1',
                                    'numCells': 5,
                                    'xRange': [0, 0.5],
                                    'yRange': [0.5, 1],
                                    'cellModel': 'HH'}

netParams.popParams['GC2'] = {'cellType': 'GC2',
                                    'cellLabel': 'GC2',
                                    'numCells': 5,
                                    'xRange': [0, 0.5],
                                    'yRange': [0.5, 1],
                                    'cellModel': 'HH'}


netParams.importCellParams( label='PYR_HH_rule',
                            conds={'cellType' : 'GC1',
                                   'cellModel': 'HH'},
	                        fileName='n83.hoc',
                            cellName='GranuleCell83',
                            importSynMechs=True)
#
netParams.importCellParams( label='2PYR_HH_rule',
                            conds={'cellType' : 'GC2',
                                   'cellModel': 'HH'},
	                        fileName='n84.hoc',
                            cellName='GranuleCell84',
                            importSynMechs=True)

# netParams.importCellParams(label='PYR_HH_rule2', conds={'cellLabel': 'GC0', 'cellModel': 'HH'},
# 	fileName='n90.hoc', cellName='GranuleCell90', importSynMechs=True)


netParams.synMechParams['AMPA'] = {'mod': 'Exp2Syn', 'tau1': 1.0, 'tau2': 5.0, 'e': 0}  # soma NMDA synapse


netParams.connParams['recurrent'] = {
	'preConds': {'pop': 'GC1'}, 'postConds': {'pop': 'GC2'},  #  PYR -> PYR random
	#'connFunc': 'convConn', 	# connectivity function (random)
	#'convergence': 'uniform(0,10)', 			# max number of incoming conns to cell
	#'weight': 0.001, 			# synaptic weight
	#'delay': 5,					# transmission delay (ms)
	'sec': 'dend_2s',
    'synMech': 'Exp2Syn_0'
    }
print(netParams.synMechParams)

simConfig = specs.SimConfig()					# object of class SimConfig to store simulation configuration
simConfig.duration = 1*1e1 			# Duration of the simulation, in ms
simConfig.dt = 0.025 				# Internal integration timestep to use
simConfig.verbose = 1			# Show detailed messages

simConfig.analysis['plot2Dnet'] = {} 			# Plot recorded traces for this list of cells


# Create network and run simulation
sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)

import pylab; pylab.show()  # this line is only necessary in certain systems where figures appear empty
