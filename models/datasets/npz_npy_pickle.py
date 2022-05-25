# template-name: NPZ/NPY/Pickle
# template-type: Файл
# <code-block> Load dataset from NPZ/NPY/Pickle file
import numpy as np

data = np.load('file.<npz/npy/pkl>', mmap_mode=None,
               allow_pickle=False, fix_imports=True, encoding='ASCII')
