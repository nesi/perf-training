import matplotlib.pyplot as plt
import numpy as np

x =     ['original'  , 'vect' , 'numba','multiproc'  , 'mpi4py'   , 'ctypes', 'openmp-c']
times = [float('nan'), 2*60+6., 1*60+4., float('nan'), 2*60+14.   , 26.     , 10.       ]

fig, ax = plt.subplots()

ind = np.arange(len(x))
plt.bar(ind, times)
ax.set_xticklabels(x)

ax.set_ylabel('Wall clock time [s]')
ax.set_title('python scatter.py -nx 256 -ny 256 -nc 256')

plt.show()