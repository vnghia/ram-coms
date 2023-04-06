import docker
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

import monitor

client = docker.from_env()


usages = np.zeros((10,))

for i in tqdm(range(usages.shape[0])):

    command = rf"""
import random
import string
import time
N = {10**(i)}
data = "".join(random.choices(string.ascii_uppercase + string.digits, k=N))
time.sleep(10)
"""

    usages[i] = monitor.monitor_mem_usage(client, "python", f"python3 -c '{command}'")

plt.plot(usages)
plt.legend()
plt.show()
