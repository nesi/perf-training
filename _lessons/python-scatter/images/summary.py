import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
 
objects = ['original'  , 'vect' , 'numba', 'ctypes', 'multiproc 8th'  , 'mpi4py 8pr', 'openmp-c 8th'   ]
y_pos = np.arange(len(objects))
times_sec = [15*60+50.   , 2*60+6., 1*60+4., 26.     ,  3*60+34.98, 2*60+14., 10.         ]
 
plt.bar(y_pos, times_sec, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Wall clock time [s]')
plt.title('Mahuika: python scatter.py -nx 256 -ny 256 -nc 256')
 
plt.show()

