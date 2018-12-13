import pandas as pd
import matplotlib.pyplot as plt

times_sec = [15*60+50.   , 2*60+6., 1*60+4., 26.     ,  3*60+34.98, 2*60+14., 10.         ]


s = pd.Series(
    	[times_sec[0]/t for t in times_sec],
    	index = ['original'  , 'vect' , 'numba', 'ctypes', 'mproc 8'  , 'mpi 8', 'omp-c 8'   ]
)

print(s)

#Set descriptions:
plt.title('Mahuika: python scatter.py -nx 256 -ny 256 -nc 256')

my_colors = ['red', 'blue', 'blue', 'blue', 'cyan', 'cyan', 'cyan']

s.plot( 
    kind='bar', 
    color=my_colors,
)
plt.ylabel('Speedup')

plt.show()

