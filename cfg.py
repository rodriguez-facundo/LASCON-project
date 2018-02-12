from netpyne import specs

# SIMULATION DEFINITIONS
cfg = specs.SimConfig()
cfg.duration = 5*1e2
cfg.dt = 0.025
cfg.hParams = {'v_init': -65}
cfg.verbose = 1

# change color for raster plot
colors = dict()
for i in range(500): colors['GC'+str(i)] = 'black'
for l, c in zip(['BC', 'MC', 'HIPP'], ['blue', 'red', 'blue']): colors[l] = c

cfg.analysis['plotRaster'] = {'popColors':colors, 'markerSize':10, 'marker': 'o'}
cfg.analysis['plot2Dnet'] = True
