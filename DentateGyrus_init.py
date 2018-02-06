from netpyne import sim

# COMMENTS
# --------
#          Here we adapted an existing computational model of the dentate gyrus
#          (https://senselab.med.yale.edu/modeldb/ShowModel.cshtml?model=155568)
#          The original model was written in hoc, and we replicated it using
#          netpyne.

# ATENTION
# --------
#          This code runs under a netpyne fork available here:
#          - https://github.com/rodriguez-facundo/netpyne

# read cfg and netParams from command line arguments if available; otherwise use default
simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='DentateGyrus_cfg.py', netParamsDefault='DentateGyrus_netParams.py')

# Create network and run simulation
sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
