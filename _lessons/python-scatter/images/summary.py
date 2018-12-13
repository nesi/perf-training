import matplotlib.pyplot as plt
import numpy as np

xlabels =     ['original'  , 'vect' , 'numba', 'ctypes', 'openmp-c 8th', 'multiproc th'  , 'mpi4py 8pr'   ]
times   =     [15*60+50.   , 2*60+6., 1*60+4., 26.     , 10.      ,  15*60+47.44, 2*60+14.   ]

fig, ax = plt.subplots()

ind = np.arange(len(xlabels))
plt.bar(ind, times)
ax.set_xticklabels(xlabels)

ax.set_ylabel('Wall clock time [s]')
ax.set_title('python scatter.py -nx 256 -ny 256 -nc 256')

plt.show()