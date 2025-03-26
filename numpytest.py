import numpy as np

z = np.arange(81).reshape(3, 3, 3, 3)
indices = (1, 1, 1, 1)
print(z[indices])
