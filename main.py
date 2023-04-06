import docker
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

import monitor


def byte_to_mb(size: int):
    return size / (1 << 20)


client = docker.from_env()


usages = np.zeros((5, 10, 2))

for i in tqdm(range(usages.shape[0])):

    command = rf"""
import random
import string
import sys
print("Hello")
N = {10**(i + 4)}
data = "".join(random.choices(string.ascii_uppercase + string.digits, k=N))
with open("/root/data_sizeof", "w") as f:
  f.write(str(sys.getsizeof(data)))
  f.flush()
while True:
  pass
"""

    container = client.containers.run(
        "python", f"python3 -c '{command}'", auto_remove=True, detach=True
    )

    sizeof_result = container.exec_run("cat /root/data_sizeof")
    while sizeof_result.exit_code:
        sizeof_result = container.exec_run("cat /root/data_sizeof")
    data_size = byte_to_mb(int(sizeof_result.output))
    usages[i, :, 1] = data_size

    for j in tqdm(range(usages.shape[1]), leave=False):
        usages[i, j] = monitor.get_container_mem_usage(container)

    container.stop()

fig = plt.figure()
gs = fig.add_gridspec(usages.shape[0], hspace=0)
axs = gs.subplots(sharex=False, sharey=True)

for i in range(usages.shape[0]):
    axs[i].plot(usages[i, :, 0])
    axs[i].plot(usages[i, :, 1], linestyle="--")
    axs[i].set_title(f"{i}")

plt.legend()
plt.show()
