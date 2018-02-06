from netpyne import specs

# SIMULATION DEFINITIONS
cfg = specs.SimConfig()
cfg.duration = 1*1e0
cfg.dt = 0.025
cfg.hParams = {'v_init': -65}
cfg.verbose = 0

# change color for raster plot
colors = dict()
for i in range(500): colors['GC'+str(i)] = 'black'
for l, c in zip(labels[:-1], ['blue', 'red', 'blue']): colors[l] = c

cfg.analysis['plotRaster'] = {'popColors':colors, 'markerSize':10, 'marker': 'o'}
cfg.analysis['plot2Dnet'] = True
