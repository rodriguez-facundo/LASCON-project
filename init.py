from netpyne import sim

# COMMENTS
# --------
#          Here we adapted an existing computational model of the dentate gyrus
#          (https://senselab.med.yale.edu/modeldb/ShowModel.cshtml?model=155568)
#          The original model was written in hoc, and we replicated it using
#          netpyne.


from netpyne import sim
from cfg import cfg
from netParams import netParams

sim.createSimulateAnalyze(netParams, cfg)
