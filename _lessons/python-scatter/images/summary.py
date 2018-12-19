import pandas as pd
import matplotlib.pyplot as plt

times_sec = [15*60+50.   , 2*60+6., 1*60+4., 26.     ,  3*60+34.98, 2*60+14., 10.         ]


df = pd.DataFrame(
    	{'speedup': [times_sec[0]/t for t in times_sec],},
    	index=['original'  , 'vect' , 'numba', 'ctypes', 'multiproc 8'  , 'mpi 8', 'openmp-c 8'   ]
)

print(df)

#Set descriptions:

my_colors = ['red', 'blue', 'blue', 'blue', 'cyan', 'cyan', 'cyan']

df.plot.bar(y='speedup',
    color=my_colors, rot=0, legend=False, fontsize=12,
)
plt.ylabel('Speedup', fontsize=12)
plt.title('Mahuika: python scatter.py -nx 256 -ny 256 -nc 256')

plt.show()

