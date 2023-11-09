import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import matplotlib as mpl



x = np.arange(0, 10, 0.1)
y = np.sin(x)

plt.plot(x, y)

plt.savefig('Graph')
img = Image.open('Graph.png')
# изменяем размер
new_image = img.resize((400, 300))
new_image.show()
# сохранение картинки
new_image.save('./Graph.png')